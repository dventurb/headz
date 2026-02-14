import pygame as pg
import pymunk as pm 
import random 

from config import WIDTH, HEIGHT, GRAVITY
from widgets import Image
from ball import Ball
from pitch import Pitch
from utility_ai import UtilityAI

class GameMenu:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock 
        self.gameStateManager = gameStateManager
        
        self.space = pm.Space()
        self.space.gravity = 0, GRAVITY

        self.ball = Ball(self.space, "assets/ball/ball_1.png", (768, 100))
        self.pitch = Pitch(self.space)
        
        self.display_score = Image("assets/display.png", (768, 100))
        
        # Sprites of each character have different sizes, so these values are used to center each one on the scoreboard. First dict represents the front sprite and the second represents the name img.
        self.display_offset = [
                    { "Bedas": 0, "Lage": -8, "João David": 10, "Valonga": -5, "Brito": -2},
                    { "Bedas": 0, "Lage": 0, "João David": 25, "Valonga": 65, "Brito": 10}
                ]

        self.timer = 90
        self.timer_event = pg.time.set_timer(pg.USEREVENT, 1000)

        self.player = None
        self.npc = None
        self.stadium = None

        self.utility_ai = UtilityAI()

        self.players = {}

        self.press_c = False
        self.play_music = False
        self.start = False


    def run(self, events):
        if self.player is None or self.npc is None:
            self.player = self.gameStateManager.selected_player
            self.player.image = Image(self.player.side_right, (384, 760))
            self.player.side = "right"
            self.player.body.position = (384, 760)        

            self.player_sprite = Image(self.player.front, (self.display_score.rect.left + 215, self.display_score.rect.top + 290 + self.display_offset[0][self.player.name]))
            w, h = self.player_sprite.image.get_size()
            self.player_sprite.image = pg.transform.smoothscale(self.player_sprite.image, (w * 0.29, h * 0.29))

            self.player_name = Image(self.player.font, (self.display_score.rect.left + 290 + self.display_offset[1][self.player.name], self.display_score.rect.top + 298))
            w, h = self.player_name.image.get_size()
            self.player_name.image = pg.transform.smoothscale(self.player_name.image, (w * 0.20, h * 0.20))

            self.npc = self.gameStateManager.npc
            self.npc.image = Image(self.npc.side_left, (1152, 760))
            self.npc.side = "left"
            self.npc.body.position = (1152, 760)
            self.npc.shape.collision_type = 6

            self.npc_sprite = Image(self.npc.front, (self.display_score.rect.right - 5, self.display_score.rect.top + 290 + self.display_offset[0][self.npc.name]))
            w, h = self.npc_sprite.image.get_size()
            self.npc_sprite.image = pg.transform.smoothscale(self.npc_sprite.image, (w * 0.29, h * 0.29))
            
            self.npc_name = Image(self.npc.font, (self.display_score.rect.right + 65 + self.display_offset[1][self.npc.name], self.display_score.rect.top + 298))
            w, h = self.npc_name.image.get_size()
            self.npc_name.image = pg.transform.smoothscale(self.npc_name.image, (w * 0.20, h * 0.20))

            self.space.add(self.player.body, self.player.shape)
            self.space.add(self.npc.body, self.npc.shape)

        if self.stadium is None:
            self.stadium = self.gameStateManager.selected_stadium
            self.stadium.image = pg.image.load(self.stadium.stadium).convert()
            self.stadium.image = pg.transform.scale(self.stadium.image, (WIDTH, HEIGHT))

        if not self.play_music:
            pg.mixer.music.load(self.stadium.sound)
            pg.mixer.music.play(-1)
            self.play_music = True
            

        self.space.step(1/60)

        for event in events:
            # Countdown timer
            # References: https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
            if event.type == pg.USEREVENT:
                if self.start and self.timer > 0:
                    self.timer -= 1 
                elif not self.start:
                    if self.timer <= 87: # 3 seconds
                        self.timer = 90
                        self.ball = Ball(self.space, "assets/ball/ball_1.png", (768, 100))
                        self.start = True
                    self.timer -= 1 
                    update_screen_countdown(self)
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
                if event.key == pg.K_x:
                    self.player.kick_high = False
                if event.key == pg.K_a:
                    self.player.lift_ball = False
                if event.key == pg.K_c:
                    self.press_c = False
                    self.player.kick_low = False
                if event.key == pg.K_x:
                    self.player.kick_high = False
                if event.key == pg.K_c:
                    self.press_c = False
                    self.player.has_ball = False


        if not self.start:
            return

        self.space.on_collision(2, 3, begin=ball_hits_pitch, data=self.ball)
        self.space.on_collision(1, 2, begin=player_with_ball, data=self)
        self.space.on_collision(2, 6, begin=npc_with_ball, data=self)
        self.space.on_collision(1, 3, begin=player_on_pitch, data=self.player)
        self.space.on_collision(3, 6, begin=npc_on_pitch, data=self.npc)
        self.space.on_collision(2, 4, begin=npc_score_goal, data=self)
        self.space.on_collision(2, 5, begin=player_score_goal, data=self)
        
        self.draw()


      # Movement the player
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]: 
            self.player.update_sprite("left")
            self.player.body.velocity = (-self.player.speed * 5, self.player.body.velocity.y)
        if keys[pg.K_RIGHT]:
            self.player.update_sprite("right")
            self.player.body.velocity = (self.player.speed * 5, self.player.body.velocity.y)
        if keys[pg.K_UP] and self.player.on_pitch:
            pg.mixer.Sound("assets/sounds/jump.mp3").play() 
            self.player.on_pitch = False
            self.player.body.velocity = (self.player.body.velocity.x, -self.player.jump * 10)    
   

       # Player have the ball and presse z or x for shoting 
        if self.player.has_ball:
            if self.player.kick_high:
                if not self.ball.body_in_space():
                    self.space.add(self.ball.body, self.ball.shape)
                if self.player.side == "left":
                    self.ball.body.position = self.player.body.position - (40, 0)
                    self.ball.body.apply_impulse_at_world_point((-self.player.shot * 2, -200), self.ball.body.position)
                elif self.player.side == "right":
                    self.ball.body.position = self.player.body.position + (40, 0)
                    self.ball.body.apply_impulse_at_world_point((self.player.shot * 2, -200), self.ball.body.position)             
                pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()
                self.player.has_ball = False
                self.press_c = False
                self.player.kick_high = False
            elif self.player.kick_low:
                if not self.ball.body_in_space():
                    self.space.add(self.ball.body, self.ball.shape)
                if self.player.side == "left":
                    self.ball.body.position = self.player.body.position - (40, 0)
                    self.ball.body.apply_impulse_at_world_point((-self.player.shot * 2, 0), self.ball.body.position)
                elif self.player.side == "right":
                    self.ball.body.position = self.player.body.position + (40, 0)
                    self.ball.body.apply_impulse_at_world_point((self.player.shot * 2, 0), self.ball.body.position)             
                pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()
                self.player.has_ball = False 
                self.press_c = False
                self.player.kick_low = False
            elif self.player.lift_ball:
                if not self.ball.body_in_space():
                    self.space.add(self.ball.body, self.ball.shape)
                if self.player.side == "left":
                    self.ball.body.position = self.player.body.position - (40, 150)
                    self.ball.body.apply_impulse_at_world_point((-20, -self.player.shot), self.ball.body.position)    
                elif self.player.side == "right":
                    self.ball.body.position = self.player.body.position + (40, -150)
                    self.ball.body.apply_impulse_at_world_point((20, -self.player.shot), self.ball.body.position)    
                pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()
                self.player.has_ball = False 
                self.press_c = False
                self.player.lift_ball = False


        # Limit the max heigh a ball can reach
        #if self.ball.body.position.y > HEIGHT:
         #   self.ball.body.position = (max(min(self.ball.body.position.x, (WIDTH - 100)), 100), 100)
        

        # Update the image of the ball when player has the ball
        if self.player.has_ball and not self.npc.has_ball:
            if self.player.side == "left":
                self.ball.image.rect.center = (self.player.body.position.x - 80, self.player.image.rect.bottom - 20)
                self.ball.body.position = (self.player.body.position.x - 80, self.ball.body.position.y)
            elif self.player.side == "right":
                self.ball.image.rect.center = (self.player.body.position.x + 80, self.player.image.rect.bottom - 20)
                self.ball.body.position = (self.player.body.position.x + 80, self.ball.body.position.y)
            self.ball.draw(self.screen)


        # Update the image of the ball when NPC has the ball
        if self.npc.has_ball and not self.player.has_ball:
            if self.npc.side == "left":
                self.ball.image.rect.center = (self.npc.body.position.x - 80, self.npc.image.rect.bottom - 20)
                self.ball.body.position = (self.npc.body.position.x - 80, self.ball.body.position.y)
            elif self.npc.side == "right":
                self.ball.image.rect.center = (self.npc.body.position.x + 80, self.npc.image.rect.bottom - 20)
                self.ball.body.position = (self.npc.body.position.x + 80, self.ball.body.position.y)
            self.ball.draw(self.screen)


        # Player drops the ball, add ball body and shape back to space
        if not self.ball.body_in_space() and not self.player.has_ball and not self.npc.has_ball:
            if self.player.side == "left":
                self.ball.body.position = (self.player.body.position.x - 80, self.player.body.position.y)
            elif self.player.side == "right":
                self.ball.body.position = (self.player.body.position.x + 80, self.player.body.position.y)
            self.space.add(self.ball.body, self.ball.shape)


    def draw(self):
        self.screen.blit(self.stadium.image, (0, 0))
        
        # Ball movement effect
        self.ball.update_sprite(int((self.ball.body.velocity.length % 4) + 1))
        
        if not self.player.has_ball and not self.npc.has_ball:
            self.ball.update()
            self.ball.draw(self.screen)

        self.display_score.draw(self.screen)

        self.player_sprite.draw(self.screen)
        self.npc_sprite.draw(self.screen)
        self.player_name.draw(self.screen)
        self.npc_name.draw(self.screen)
        
        font = pg.font.Font("assets/fonts/shineseiya.ttf", 140)
        self.screen.blit(font.render(str(self.timer).rjust(3), True, (255, 255, 255)), (690, 20))
        
        font = pg.font.Font("assets/fonts/shineseiya.ttf", 80)
        self.screen.blit(font.render(str(self.player.score).rjust(3), True, (255, 255, 255)), (600, 80))
        self.screen.blit(font.render(str(self.npc.score).rjust(3), True, (255, 255, 255)), (840, 80))

        self.player.update()
        self.player.draw(self.screen)

        self.utility_ai.update(self.ball, self.player, self.npc)
        self.utility_ai.execute_action(self.ball, self.npc, self.space)
        #print(self.utility_ai.action)
        #print(self.utility_ai.role)

        self.npc.update()
        self.npc.draw(self.screen)


def reset_after_goal(self, side):
    if side == "LEFT":
        self.ball.body.position = (300, 100)
    elif side == "RIGHT":
        self.ball.body.position = (WIDTH - 300, 100);

    self.player.body.position = (384, 760)        
    self.player.update()
    self.player.draw(self.screen)

    self.npc.body.position = (1152, 760)
    self.npc.update()
    self.npc.draw(self.screen)


# Callback for collision between the ball and the pitch
# Used to play sound of the ball hits the ground.
def ball_hits_pitch(arbiter, space, data):
    pg.mixer.Sound("assets/sounds/ball_drop.mp3").play() 
    #data.body.velocity = (random.choice([100, -100]), data.body.velocity.y)
    return True


# Callback collision between player and the ball
# Used to detect if the user press z, x, c keys when the player touches the ball.
def player_with_ball(arbiter, space, data):
    if data.player.kick_low:
        if data.player.side == "left":
            data.ball.body.position = data.player.body.position - (40, 0)
            data.ball.body.apply_impulse_at_world_point((-data.player.shot * 2, 0), data.ball.body.position)
        elif data.player.side == "right":
            data.ball.body.position = data.player.body.position + (40, 0)
            data.ball.body.apply_impulse_at_world_point((data.player.shot * 2, 0), data.ball.body.position)         
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()
    
    elif data.player.kick_high:
        if data.player.side == "left":
            data.ball.body.position = data.player.body.position - (40, 0)
            data.ball.body.apply_impulse_at_world_point((-data.player.shot * 2, -200), data.ball.body.position)
        elif data.player.side == "right":
            data.ball.body.position = data.player.body.position + (40, 0)
            data.ball.body.apply_impulse_at_world_point((data.player.shot * 2, -200), data.ball.body.position)    
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()

    elif data.player.lift_ball:
        if data.player.side == "left":
            data.ball.body.position = data.player.body.position - (40, 150)
            data.ball.body.apply_impulse_at_world_point((-20, -data.player.shot), data.ball.body.position)    
        elif data.player.side == "right":
            data.ball.body.position = data.player.body.position + (40, -150)
            data.ball.body.apply_impulse_at_world_point((20, -data.player.shot), data.ball.body.position)  
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()

    elif data.press_c and not data.npc.has_ball:
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
    npc = data
    npc.on_pitch = True
    return True


# Callback collision ball with left wall 
# Ball hits the left wall, goal from the npc.
def npc_score_goal(arbiter, space, data):        
    pg.mixer.Sound("assets/sounds/goal.mp3").play()
    data.npc.score += 1 
    reset_after_goal(data, "LEFT")
    return False


# Callback collision ball with right wall
# Ball hits the right wall, goal from the player.
def player_score_goal(arbiter, space, data):
    pg.mixer.Sound("assets/sounds/goal.mp3").play()
    data.player.score += 1
    reset_after_goal(data, "RIGHT")
    return False


def update_screen_countdown(self):
    self.screen.blit(self.stadium.image, (0, 0))
    self.display_score.draw(self.screen)
    self.player_sprite.draw(self.screen)
    self.npc_sprite.draw(self.screen)
    self.player_name.draw(self.screen)
    self.npc_name.draw(self.screen)
    font = pg.font.Font("assets/fonts/shineseiya.ttf", 140)
    self.screen.blit(font.render(str(90).rjust(3), True, (255, 255, 255)), (690, 20))
    font = pg.font.Font("assets/fonts/shineseiya.ttf", 80)
    self.screen.blit(font.render(str(self.player.score).rjust(3), True, (255, 255, 255)), (600, 80))
    self.screen.blit(font.render(str(self.npc.score).rjust(3), True, (255, 255, 255)), (840, 80))
    self.player.draw(self.screen)
    self.npc.draw(self.screen)                    
    countdown = Image(f"assets/countdown/{abs(self.timer - 90)}.png", ((WIDTH / 2), 400))
    countdown.draw(self.screen)
    pg.mixer.Sound("assets/sounds/countdown.mp3").play()
