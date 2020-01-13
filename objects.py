import pygame
import os


sizes = width, height = 1000, 500
screen = pygame.display.set_mode(sizes)


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


class Hero(pygame.sprite.Sprite):
    image = load_image("falcon.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Hero.image
        self.rect = self.image.get_rect()

    def update(self, args1):
        self.rect.y = args1[1]
        self.rect.x = args1[0]


all_sprites = pygame.sprite.Group()

for _ in range(1):
    Hero(all_sprites)
x_speed = 0
y_speed = 0
running = True
while running:
    all_sprites.update([x_speed, y_speed])
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if keystate[pygame.K_LEFT]:
            x_speed -= 10
        if keystate[pygame.K_RIGHT]:
            x_speed += 10
        all_sprites.update([x_speed, y_speed])
    screen.fill(pygame.Color('white'))
    all_sprites.draw(screen)
    all_sprites.update([x_speed, y_speed])
    pygame.display.flip()
pygame.quit()