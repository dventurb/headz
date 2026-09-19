import pygame as pg
import pymunk as pm 
import random 

from core.config import WIDTH, HEIGHT, GRAVITY
from ui.widgets import Image
from entities.ball import Ball
from entities.pitch import Pitch
from entities.player import Side
from ai.utility_ai import UtilityAI

class GameplayScreen:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock 
        self.gameStateManager = gameStateManager
       
        # pymunk
        self.space = pm.Space()
        self.space.gravity = 0, GRAVITY

        self.ball = Ball(self.space, "assets/ball/ball_1.png", (768, 100))
        self.pitch = Pitch(self.space)
        
        self.display_score = Image("assets/display.png", (768, 100))

        self.jump_sound = pg.mixer.Sound("assets/sounds/jump.mp3")
        self.kick_sound = pg.mixer.Sound("assets/sounds/ball_kick.mp3")
        self.ball_sound = pg.mixer.Sound("assets/sounds/ball_drop.mp3")
        self.goal_sound = pg.mixer.Sound("assets/sounds/goal.mp3")
        self.countdown_sound = pg.mixer.Sound("assets/sounds/countdown.mp3")
        self.start_whistle_sound = pg.mixer.Sound("assets/sounds/start_whistle.mp3")
        self.final_whistle_sound = pg.mixer.Sound("assets/sounds/final_whistle.mp3")

        self.big_font = pg.font.Font("assets/fonts/shineseiya.ttf", 140)
        self.small_font = pg.font.Font("assets/fonts/shineseiya.ttf", 80)

        # Sprites of each character have different sizes, so these values are used to center each one on the scoreboard. First dict represents the front sprite and the second represents the name img.
        self.display_offset = [
                    { "Bedas": 0, "Lage": -8, "João David": 10, "Valonga": -5, "Brito": -2},
                    { "Bedas": 0, "Lage": 0, "João David": 25, "Valonga": 65, "Brito": 10}
                ]

        self.game_timer = 90
        self.countdown_timer = 3
        self.timer_event = pg.time.set_timer(pg.USEREVENT, 1000)

        self.player = None
        self.npc = None
        self.stadium = None

        self.utility_ai = UtilityAI()

        self.players = {}

        self.press_c = False
        self.play_music = False
        self.start_game = False
        self.end_game = False


    def run(self, events):
        dt = self.clock.tick(60) / 1000

        if self.player is None or self.npc is None:
            self.initialize_game()
            self.setup_collisions()

        if self.stadium is None:
            self.load_stadium()
    
        self.handle_events(events)
        
        self.handle_movement_input()
        self.update_ai(dt)
        self.handle_player_actions()
        self.update_game(dt)

        self.space.step(dt)

        self.draw()


    def draw(self):
        if not self.start_game:
            return 

        self.screen.blit(self.stadium.image, (0, 0))
        
        # Ball movement effect
        self.ball.update_sprite(int((self.ball.body.velocity.length % 4) + 1))
        
        if not self.player.has_ball and not self.npc.has_ball:
            self.ball.update()

        self.display_score.draw(self.screen)

        self.player_sprite.draw(self.screen)
        self.npc_sprite.draw(self.screen)
        self.player_name.draw(self.screen)
        self.npc_name.draw(self.screen)
        
        self.screen.blit(self.big_font.render(str(self.game_timer).rjust(3), True, (255, 255, 255)), (690, 20))
        self.screen.blit(self.small_font.render(str(self.player.score).rjust(3), True, (255, 255, 255)), (600, 80))
        self.screen.blit(self.small_font.render(str(self.npc.score).rjust(3), True, (255, 255, 255)), (840, 80))

        self.player.update()
        self.player.draw(self.screen)

        self.npc.update()
        self.npc.draw(self.screen)
            
        self.ball.draw(self.screen)

   
    def initialize_game(self):
        self.setup_player()
        self.setup_npc()


    def load_stadium(self):
        self.stadium = self.gameStateManager.selected_stadium
        self.stadium.image = pg.image.load(self.stadium.stadium).convert()
        self.stadium.image = pg.transform.scale(self.stadium.image, (WIDTH, HEIGHT))
        
        # Background sound 
        if not self.play_music:
            pg.mixer.music.load(self.stadium.sound)
            pg.mixer.music.play(-1)
            self.play_music = True


    def handle_events(self, events):
        for event in events:
            
            # Countdown timer
            # References: https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
            if event.type == pg.USEREVENT:
                if self.start_game:
                    if self.game_timer > 0:
                        self.game_timer -= 1 

                    else:
                        self.final_whistle_sound.play()

                else:
                    if self.countdown_timer > 0:
                        self.update_screen_countdown()
                        self.countdown_timer -= 1 

                    else:
                        self.start_whistle_sound.play()
                        self.ball.body.position = (768, 100)
                        self.ball.body.velocity = (0, 0)
                        self.start_game = True


            # Check when z, x, c keys was pressed (KEYDOWN) and released (KEYUP)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.player.kick_low = True

                if event.key == pg.K_x:
                    self.player.kick_high = True
                
                if event.key == pg.K_a:
                    self.player.lift_ball = True

                if event.key == pg.K_c:
                    self.press_c = True
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_z:
                    self.player.kick_low = False

                elif event.key == pg.K_x:
                    self.player.kick_high = False

                elif event.key == pg.K_a:
                    self.player.lift_ball = False

                elif event.key == pg.K_c:
                    self.press_c = False
                    self.player.has_ball = False


    def handle_movement_input(self):
        if not self.start_game:
            return

        # Movement the player
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]: 
            self.player.update_sprite(Side.LEFT)
            self.player.body.velocity = (-self.player.speed * 5, self.player.body.velocity.y)
        
        elif keys[pg.K_RIGHT]:
            self.player.update_sprite(Side.RIGHT)
            self.player.body.velocity = (self.player.speed * 5, self.player.body.velocity.y)
        
        else: 
            self.player.body.velocity = (0, self.player.body.velocity.y)

        if keys[pg.K_UP] and self.player.on_pitch:
            self.jump_sound.play() 
            self.player.on_pitch = False
            self.player.body.velocity = (self.player.body.velocity.x, -self.player.jump * 10)    

    def update_game(self, dt):
        if not self.start_game:
            return

        self.keep_ball_in_game()

        # Update the image of the ball when player has the ball
        if self.player.has_ball and not self.npc.has_ball:
            self.attach_ball_to_player(self.player)
            #self.ball.draw(self.screen)

        # Update the image of the ball when NPC has the ball
        if self.npc.has_ball and not self.player.has_ball:
            self.attach_ball_to_player(self.npc)
            #self.ball.draw(self.screen)

        # Player drops the ball, add ball body and shape back to space
        if not self.ball.body_in_space() and not self.player.has_ball and not self.npc.has_ball:
            direction = self.player.side.direction()

            self.ball.body.position = (self.player.body.position.x + direction * 80, self.player.body.position.y)
            self.space.add(self.ball.body, self.ball.shape)
    
    
    def update_ai(self, dt):
        if not self.start_game:
            return

        self.utility_ai.update(self.ball, self.player, self.npc)
        self.utility_ai.execute_action(self.ball, self.npc, self.space)
        #print(self.utility_ai.action)
        #print(self.utility_ai.role)


    def handle_player_actions(self):
        if not self.player.has_ball:
            return

        if self.player.kick_high:
            self.kick_ball(self.player, True)

        elif self.player.kick_low:
            self.kick_ball(self.player, False)

        elif self.player.lift_ball:
            self.lift_ball(self.player)


    def kick_ball(self, player, high):
        if not self.ball.body_in_space():
            self.space.add(self.ball.body, self.ball.shape)
           
        offset = player.side.offset()
        direction = player.side.direction()

        self.ball.body.position = player.body.position + (offset, 0)

        if high:
            impulse = (direction * player.shot * 2, -200)
        else:
            impulse = (direction * player.shot * 2, 0)

        self.ball.body.apply_impulse_at_world_point(impulse, self.ball.body.position)
        self.kick_sound.play()
        
        self.press_c = False
        player.reset_actions()


    def lift_ball(self, player):
        if not self.ball.body_in_space():
            self.space.add(self.ball.body, self.ball.shape)
        
        direction = player.side.direction()

        self.ball.body.position = player.body.position + (direction * 40, -150)
        
        impulse = (direction * 20, -player.shot)

        self.ball.body.apply_impulse_at_world_point(impulse, self.ball.body.position)    
        self.kick_sound.play()

        self.press_c = False
        player.reset_actions()


    def reset_after_goal(self, side : Side):
        self.press_c = False 
        self.player.reset_actions()
        self.npc.reset_actions()

        # reset ball positon
        if side == Side.LEFT:
            self.ball.body.position = (400, 100)
        elif side == Side.RIGHT:
            self.ball.body.position = (WIDTH - 400, 100)

        self.player.body.position = (300, 760)        
        self.npc.body.position = (WIDTH - 300, 760)
       
        self.ball.body.velocity = (0, 0)
        self.player.body.velocity = (0, 0)
        self.npc.body.velocity = (0, 0)

        self.player.on_pitch = True 
        self.npc.on_pitch = True

        if not self.ball.body_in_space():
            self.space.add(self.ball.body, self.ball.shape)

        self.ball.update()
        self.player.update()
        self.npc.update()
        
        #self.player.draw(self.screen)
        #self.npc.draw(self.screen)


    def attach_ball_to_player(self, player):
        direction = player.side.direction()
        
        self.ball.image.rect.center = (player.body.position.x + direction * 80, player.image.rect.bottom - 20)

        self.ball.body.position = (player.body.position.x + direction * 80, self.ball.body.position.y)
        self.ball.update()


    def update_screen_countdown(self):
        self.screen.blit(self.stadium.image, (0, 0))
        self.display_score.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.npc_sprite.draw(self.screen)
        self.player_name.draw(self.screen)
        self.npc_name.draw(self.screen)
        self.screen.blit(self.big_font.render(str(90).rjust(3), True, (255, 255, 255)), (690, 20))
        self.screen.blit(self.small_font.render(str(self.player.score).rjust(3), True, (255, 255, 255)), (600, 80))
        self.screen.blit(self.small_font.render(str(self.npc.score).rjust(3), True, (255, 255, 255)), (840, 80))
        self.player.draw(self.screen)
        self.npc.draw(self.screen)                    
        countdown = Image(f"assets/countdown/{self.countdown_timer}.png", ((WIDTH / 2), 400))
        countdown.draw(self.screen)
        self.countdown_sound.play()


    def setup_collisions(self):
        self.space.on_collision(2, 3, begin=ball_hits_pitch, data=self)
        self.space.on_collision(1, 2, begin=player_with_ball, data=self)
        self.space.on_collision(2, 6, begin=npc_with_ball, data=self)
        self.space.on_collision(1, 3, begin=player_on_pitch, data=self.player)
        self.space.on_collision(3, 6, begin=npc_on_pitch, data=self.npc)
        self.space.on_collision(2, 4, begin=npc_score_goal, data=self)
        self.space.on_collision(2, 5, begin=player_score_goal, data=self)


    def setup_player(self):
        self.player = self.gameStateManager.selected_player
        self.player.image = Image(self.player.side_right, (384, 760))
        self.player.side = Side.RIGHT
        self.player.body.position = (384, 760)        

        self.player_sprite = Image(self.player.front, (self.display_score.rect.left + 215, self.display_score.rect.top + 290 + self.display_offset[0][self.player.name]))
        w, h = self.player_sprite.image.get_size()
        self.player_sprite.image = pg.transform.smoothscale(self.player_sprite.image, (w * 0.29, h * 0.29))

        self.player_name = Image(self.player.font, (self.display_score.rect.left + 290 + self.display_offset[1][self.player.name], self.display_score.rect.top + 298))
        w, h = self.player_name.image.get_size()
        self.player_name.image = pg.transform.smoothscale(self.player_name.image, (w * 0.20, h * 0.20))

        self.space.add(self.player.body, self.player.shape)


    def setup_npc(self):
        self.npc = self.gameStateManager.npc
        self.npc.image = Image(self.npc.side_left, (1152, 760))
        self.npc.side = Side.LEFT
        self.npc.body.position = (1152, 760)
        self.npc.shape.collision_type = 6

        self.npc_sprite = Image(self.npc.front, (self.display_score.rect.right - 5, self.display_score.rect.top + 290 + self.display_offset[0][self.npc.name]))
        w, h = self.npc_sprite.image.get_size()
        self.npc_sprite.image = pg.transform.smoothscale(self.npc_sprite.image, (w * 0.29, h * 0.29))
        
        self.npc_name = Image(self.npc.font, (self.display_score.rect.right + 65 + self.display_offset[1][self.npc.name], self.display_score.rect.top + 298))
        w, h = self.npc_name.image.get_size()
        self.npc_name.image = pg.transform.smoothscale(self.npc_name.image, (w * 0.20, h * 0.20))

        self.space.add(self.npc.body, self.npc.shape)


    def keep_ball_in_game(self):
        x, y = self.ball.body.position 

        margin = 50

        if x < -margin or x > WIDTH + margin or y > HEIGHT + 50 or y < -margin:
            self.ball.body.position = (WIDTH / 2, 100)
            self.ball.body.velocity = (0, 0)


# Callback for collision between the ball and the pitch
# Used to play sound of the ball hits the ground.
def ball_hits_pitch(arbiter, space, data):
    if data.start_game:
        data.ball_sound.play() 
    
    #data.ball.body.velocity = (random.choice([100, -100]), data.body.velocity.y)
    return True


# Callback collision between player and the ball
# Used to detect if the user press c key when the player touches the ball.
def player_with_ball(arbiter, space, data):
    if data.press_c and not data.npc.has_ball:
        data.player.has_ball = True
        data.space.remove(data.ball.body, data.ball.shape)

    return True


def npc_with_ball(arbiter, space, data):
    data.touch_ball = True
    return True


# Callback collision between player and the pitch
# If the player is not on the ground, cannot jump.
def player_on_pitch(arbiter, space, data):
    data.on_pitch = True
    return True

def npc_on_pitch(arbiter, space, data):
    data.on_pitch = True
    return True


# Callback collision ball with left wall 
# Ball hits the left wall, goal from the npc.
def npc_score_goal(arbiter, space, data):        
    data.goal_sound.play()
    data.npc.score += 1 
    print("npc score")  # Debug
    data.reset_after_goal(Side.LEFT)
    return False


# Callback collision ball with right wall
# Ball hits the right wall, goal from the player.
def player_score_goal(arbiter, space, data):
    data.goal_sound.play()
    data.player.score += 1
    print("player score")  # Debug
    data.reset_after_goal(Side.RIGHT)
    return False
