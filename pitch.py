import pymunk as pm

from config import WIDTH, HEIGHT

class Pitch:
    def __init__(self, space):
        self.body = pm.Body(body_type=pm.Body.STATIC) 

        self.pitch = pm.Segment(self.body, (0, 860), (WIDTH, 860), 10)
        
        self.left_wall = pm.Segment(self.body, (0, 0), (0, HEIGHT), 10)
        self.right_wall = pm.Segment(self.body, (WIDTH, 0), (WIDTH, HEIGHT), 10)

        self.pitch.friction = 0.6
        self.pitch.elasticity = 0.5
        self.pitch.collision_type = 3
       
        for i in (self.left_wall, self.right_wall):
            i.friction = 0
            i.elasticity = 0.8
            
        # Different type to see who is the player that score
        self.left_wall.collision_type = 4
        self.right_wall.collision_type = 5 

        space.add(self.body, self.pitch, self.left_wall, self.right_wall) # Static bodies don't add the body to the space

