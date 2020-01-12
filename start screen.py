import pygame
import os
import random

sizes = 1536, 864
screen = pygame.display.set_mode(sizes)
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


class start_screen(pygame.sprite.Sprite):
    image = load_image("start screen.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = start_screen.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(300)
        self.rect.y = random.randrange(300)

    def update(self, args):
        self.rect.y = args[1]
        self.rect.x = args[0]


class Button(pygame.sprite.Sprite):
    back_ground = load_image('back_ground.png')

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = start_screen.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(300)
        self.rect.y = random.randrange(300)

    def update_back_ground(self, args1):
        self.rect.y = args1[1]
        self.rect.x = args1[0]


all_sprites_start_screen = pygame.sprite.Group()
all_sprites_back_ground = pygame.sprite.Group()
sprites = pygame.sprite.Group()

for _ in range(1):
    start_screen(all_sprites_start_screen)

for _ in range(1):
    Button(all_sprites_back_ground)

x_speed = - 1536
y_speed = 0
running = True
v = 700
FPS = 150
count = 0
flag_button = False

while running:
    all_sprites_start_screen.update([x_speed, y_speed])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Button.update_back_ground()
                x_speed = - 1536
                y_speed = 0
                count = 0

                if count < 1535:
                    x_speed += v / FPS
                    y_speed += 0
                    all_sprites_back_ground.update_back_ground([x_speed, y_speed])
                    count += v / FPS
                else:
                    v = 0
                    x_speed += v / FPS
                    y_speed += 0
                    all_sprites_back_ground.update_back_ground([x_speed, y_speed])
                    flag_button = True
    if count < 1535:
        x_speed += v / FPS
        y_speed += 0
        all_sprites_start_screen.update([x_speed, y_speed])
        count += v / FPS
    else:
        v = 0
        x_speed += v / FPS
        y_speed += 0
        all_sprites_start_screen.update([x_speed, y_speed])
        flag_button = True
    if flag_button:
        sprites.add(Button(pygame.Color('dodgerblue'),
                            pygame.Color('lightgreen'),
                            pygame.Rect(300, 200, 90, 100),
                            lambda b: print(f"Click me again!"),
                            'Another'))
    screen.fill(pygame.Color('black'))
    all_sprites_start_screen.draw(screen)
    all_sprites_start_screen.update([x_speed, y_speed])
    clock.tick(FPS)
    pygame.display.flip()
