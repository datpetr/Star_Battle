import pygame
import os
import sys


pygame.init()
size = width, height = 600, 1000
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

# группы спрайтов


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
flag = True

tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)
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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


camera = Camera()


clock = pygame.time.Clock()


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
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


player, level_x, level_y = generate_level(load_level('map.txt'))


start_screen()

fps = 600
v = 60

running = True
while running:
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Нажатие стрелок
            if event.key == pygame.K_UP:
                player.up()
            if event.key == pygame.K_DOWN:
                player.down()
            if event.key == pygame.K_LEFT:
                player.left()
            if event.key == pygame.K_RIGHT:
                player.right()
        elif event.type == pygame.KEYUP:
            player.stop()
        all_sprites.update(event)
    player.move()
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    player_group.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()