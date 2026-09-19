import pymunk as pm

from core.config import WIDTH, HEIGHT

class Pitch:
    def __init__(self, space):
        self.body = pm.Body(body_type=pm.Body.STATIC) 

        self.pitch = pm.Segment(self.body, (0, 860), (WIDTH, 860), 10)
        self.pitch.friction = 0.6
        self.pitch.elasticity = 0.5
        self.pitch.collision_type = 3
       
        self.left_wall = pm.Segment(self.body, (0, 0), (0, HEIGHT), 10)
        self.right_wall = pm.Segment(self.body, (WIDTH, 0), (WIDTH, HEIGHT), 10)

        for i in (self.left_wall, self.right_wall):
            i.friction = 0
            i.elasticity = 0.8

        # Goal sensor 
        self.left_goal = pm.Poly(self.body, [(0, 0), (40, 0), (40, HEIGHT), (0, HEIGHT)]) 
        self.left_goal.sensor = True 

        self.right_goal = pm.Poly(self.body, [(WIDTH - 40, 0), (WIDTH, 0), (WIDTH, HEIGHT), (WIDTH - 40, HEIGHT)]) 
        self.right_goal.sensor = True 
            
        # Different type to see who is the player that score
        self.left_goal.collision_type = 4
        self.right_goal.collision_type = 5 

        space.add(self.body, self.pitch, self.left_wall, self.right_wall, self.left_goal, self.right_goal) # Static bodies don't add the body to the space

