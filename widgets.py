import pygame as pg

# References: https://www.youtube.com/watch?v=8SzTzvrWaAA
class Button:
    def __init__(self, text, color, width, height, pos):
        # Top rectangle
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = color 

        # Text 
        font = pg.font.Font(None, 30)
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self, screen):
        pg.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)
