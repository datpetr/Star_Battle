import pygame
import os
import sys



pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
rect = screen.get_rect()  # создается Rect


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if colorkey is not None:
        image = pygame.image.load(fullname).convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        # Оставляем картинку прозрачной
        image = pygame.image.load(fullname).convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
flag = True

player_boba_fet = load_image('boba_fet_1.png')
player_darth_vader = load_image('darth_vader.png')
player_nazgy = load_image('nazgy.png')

tile_width = 920
tile_height = 540


class Choice_players(pygame.sprite.Sprite, gui.Dialog):
    image = load_image("start_fon.png")

    def __init__(self):
        self.image = Choice_players.image
        self.rect = self.image.get_rect()

    def update(self, args):
        self.rect.y = args1[1]
        self.rect.x = args1[0]

for i in range(1):
    Choice_players(all_sprites)


class Player1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player1
        self.rect = self.image.get_rect().move(10 * pos_x + 15,
                                               10 * pos_y + 5)
        self.mx = 0
        self.my = 0
    # Функции движения

    def move(self):
        self.rect[0] += self.mx
        self.rect[1] += self.my

    def up(self):
        if ((self.rect[0] + self.mx < 500)
                and (self.rect[1] + self.my < 500)):
            self.mx = 0
            self.my = -1

    def down(self):
        if ((self.rect[0] + self.mx < 500)
                and (self.rect[1] + self.my < 500)):
            self.mx = 0
            self.my = 1

    def stop(self):
        if ((self.rect[0] + self.mx < 500)
                and (self.rect[1] + self.my < 500)):
            self.mx = 0
            self.my = 0

    def right(self):
        if ((self.rect[0] + self.mx < 500)
                and (self.rect[1] + self.my < 500)):
            self.mx = 1
            self.my = 0

    def left(self):
        if ((self.rect[0] + self.mx < 500)
                and (self.rect[1] + self.my < 500)):
            self.mx = -1
            self.my = 0


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


camera = Camera()


clock = pygame.time.Clock()


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Rules: game without rules :-)",
                  ""]

    fon = pygame.transform.scale(load_image('star_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == \
                    pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


start_screen()

fps = 600
v = 200
count = 0
x_speed = - 2000
y_speed = 0
flag = True

while flag:
    all_sprites.update([x_speed, y_speed])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
    if count < 599:
        x_speed += v / FPS
        y_speed += 0
        all_sprites.update([x_speed, y_speed])
        count += v / FPS
    else:
        v = 0
        x_speed += v / FPS
        y_speed += 0
        all_sprites.update([x_speed, y_speed])
    screen.fill(pygame.Color('blue'))
    all_sprites.draw(screen)
    all_sprites.update([x_speed, y_speed])
    pygame.display.flip()


running = True
while running:
    camera.update(Player1)
    for sprite in all_sprites:
        camera.apply(sprite)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Нажатие стрелок
            if event.key == pygame.K_UP:
                Player1.up()
            if event.key == pygame.K_DOWN:
                Player1.down()
            if event.key == pygame.K_LEFT:
                Player1.left()
            if event.key == pygame.K_RIGHT:
                Player1.right()
        elif event.type == pygame.KEYUP:
            Player1.stop()
        all_sprites.update(event)
    Player1.move()
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    player_group.draw(screen)
    clock.tick(fps)
    pygame.display.flip()