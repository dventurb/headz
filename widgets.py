import pygame as pg

# References: https://www.youtube.com/watch?v=8SzTzvrWaAA
class Button:
    def __init__(self, text, color, width, height, pos):
        self.pressed = False

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

    def on_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: 
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        if event.type == pg.MOUSEBUTTONUP and self.pressed == True:
            self.callback()
            self.pressed = False


class ButtonImage:
    def __init__(self, image, position, callback):
        self.pressed = False
        self.image = image 
        self.rect = image.get_rect(topleft=position)
        self.callback = callback

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def normal(self, normal):
        self.image = normal
        pg.mouse.set_cursor()

    def hover(self, hover):
        self.image = hover
        pg.mouse.set_cursor(hand)

    def pressed(self, pressed):
        self.image = pressed


    def on_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: 
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        if event.type == pg.MOUSEBUTTONUP and self.pressed == True:
            self.callback()
            self.pressed = False

