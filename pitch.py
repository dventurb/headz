import pymunk as pm

from config import WIDTH, HEIGHT

class Pitch:
    def __init__(self, space):
        self.body = pm.Body(body_type=pm.Body.STATIC) 

        self.pitch = pm.Segment(self.body, (0, 860), (WIDTH, 860), 1)
        
        self.left_wall = pm.Segment(self.body, (0, 0), (0, HEIGHT), 1)
        self.right_wall = pm.Segment(self.body, (WIDTH, 0), (WIDTH, HEIGHT), 1)
       
        for i in (self.pitch, self.left_wall, self.right_wall):
            i.friction = 1.0
            i.elasticity = 0.8
            i.collision_type = 3

        space.add(self.body, self.pitch, self.left_wall, self.right_wall) # Static bodies don't add the body to the space

