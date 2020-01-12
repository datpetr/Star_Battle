import pygame
import os
import sys

from pygame.examples.audiocapture import callback

pygame.init()
size = width, height = 1536, 864
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
rect = screen.get_rect()
clock = pygame.time.Clock()


def load_image(name, colorkey=None, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Background(pygame.sprite.Sprite):
    image = load_image("start screen.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Background.image
        self.rect = self.image.get_rect()

    def update(self, args1):
        self.rect.y = 0
        self.rect.x = 0


class Button(pygame.sprite.Sprite):
    def __init__(self, color, color_hover, rect, callback, text='', outline=None):
        super().__init__()
        self.image = self.org
        self.rect = rect
        self.callback = callback
        self.hov = None
        self.org = None
        self.text = text

    def update(self, events):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        self.image = self.hov if hit else self.org

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                self.callback(self)


all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()

buttons.add(Button(pygame.Color('white'),
                   pygame.Rect(150, 200, 90, 100),
                   'Play',
                   pygame.Color('black')))
buttons.add(Button(pygame.Color('white'),
                   pygame.Rect(300, 200, 90, 100),
                   'Rules'))

for _ in range(1):
    Background(all_sprites)


x_speed = - 600
y_speed = 0
running = True
v = 200
FPS = 500
count = 0
while running:
    all_sprites.update([x_speed, y_speed])

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        hit = rect.collidepoint(pos)
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('blue'))
    all_sprites.draw(screen)
    all_sprites.update([x_speed, y_speed])
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)