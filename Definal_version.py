import sys
import time

import self as self
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit

best_score = [0]
coins = 0


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        # подгружаем файл из designer

        # подключаем кнопки
        self.play.clicked.connect(self.Show_lvl)
        self.rules.clicked.connect(self.Show_rules)

        print_text = QPlainTextEdit(self)
        print_text.resize(181, 51)
        print_text.move(730, 189)
        print_text.appendPlainText(str(max(best_score)))

    def Show_lvl(self):
        self.lvl = LEVEL()
        self.lvl.show()

    def Show_rules(self):
        self.rules = Rules()
        self.rules.show()


class Rules(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = Menu()
        uic.loadUi('rules.ui', self)


class LEVEL(QMainWindow):
    global best_score

    def __init__(self):
        super().__init__()
        # подгружаем файл из designer
        uic.loadUi('levels.ui', self)
        self.flag_playing = True

        # подключаем кнопки
        self.lvl1.clicked.connect(self.Show_lvl1)
        self.lvl2.clicked.connect(self.Show_lvl2)
        self.lvl3.clicked.connect(self.Show_lvl3)

    def Show_lvl1(self):
        if self.flag_playing:
            import pygame
            import random
            from os import path

            def load_image(name, colorkey=None):
                fullname = path.join('data', name)
                if colorkey is not None:
                    image = pygame.image.load(fullname).convert()
                    if colorkey == -1:
                        colorkey = image.get_at((0, 0))
                    image.set_colorkey(colorkey)
                else:
                    image = pygame.image.load(fullname).convert_alpha()
                return image

            img_dir = path.join(path.dirname(__file__), 'sounds')

            size = WIDTH, HEIGHT = [1536, 864]
            screen = pygame.display.set_mode(size)
            FPS = 60
            x_pos = 1450
            y_pos = 50

            # Задаем цвета
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            colors = [(255, 255, 255), (0, 0, 255),
                      (30, 144, 255), (255, 69, 0),
                      (255, 255, 0)]
            count_of_life = 100
            count_of_bullet = 0
            # Создаем игру и окно
            pygame.init()
            pygame.mixer.init()
            pygame.display.set_caption("STAR BATTLE")
            clock = pygame.time.Clock()
            sounds = path.join(path.dirname(__file__), 'sounds')

            # Загрузка всей игровой графики и всех звуков
            player_img = load_image('falcon.png')
            bullet_img = load_image("laser.png")
            enemy_img = load_image('ship_siths.png')
            enemy_bullet = load_image('shot_empire.png')
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            hit_sound = pygame.mixer. \
                Sound(path.join(sounds, 'hit.wav'))
            break_sound = pygame.mixer. \
                Sound(path.join(sounds, 'break.wav'))
            fly_sound = pygame.mixer. \
                Sound(path.join(sounds, 'fly.wav'))
            Order66 = pygame.mixer. \
                Sound(path.join(sounds, 'Order-66.wav'))
            Break_falcon = pygame.mixer. \
                Sound(path.join(sounds, 'break_falcon.wav'))
            anim = {'lg': [], 'sm': []}

            # обработка анимации взрыва(разрезаем
            # картинку на более маленькие картинки)
            for j in range(4):
                for i in range(8):
                    img = load_image('explosions.png')
                    rect = pygame.Rect(0, 0, img.get_width() // 8,
                                       img.get_height() // 4)
                    anim['lg'].append(img.subsurface(pygame.Rect(
                        (rect.w * i, rect.h * j), rect.size)))
                    anim['sm'].append(img.subsurface(pygame.Rect(
                        (rect.w * i, rect.h * j), rect.size)))

            class Ship(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    self.shield = 100
                    self.image = pygame.transform.scale(player_img, (130, 150))
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.centerx = WIDTH / 2
                    self.rect.bottom = HEIGHT - 10
                    self.speedx = 0

                def update(self):
                    self.speedx = 0
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_LEFT]:
                        self.speedx = -8
                    if keystate[pygame.K_RIGHT]:
                        self.speedx = 8
                    self.rect.x += self.speedx
                    if self.rect.right > WIDTH:
                        self.rect.right = WIDTH
                    if self.rect.left < 0:
                        self.rect.left = 0

                def shoot(self):
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

            class Meteor(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    meteor_list = ['meteor.png', 'meteor2.png', 'meteor4.png']
                    self.image_orig = \
                        load_image(meteor_list
                                   [random.randint(0, 2)])
                    self.image_orig.set_colorkey(BLACK)
                    self.image = self.image_orig.copy()
                    self.rect = self.image.get_rect()
                    self.radius = int(self.rect.width * .85 / 2)
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-150, -100)
                    self.speedy = random.randrange(1, 3)
                    self.speedx = random.randrange(-1, 1)
                    self.rot = 0
                    self.rot_speed = random.randrange(-5, 5)
                    self.last_update = pygame.time.get_ticks()

                def update(self):
                    self.rect.x += self.speedx
                    self.rect.y += self.speedy
                    if self.rect.top > HEIGHT + 10 or \
                            self.rect.left < -25 or \
                            self.rect.right > WIDTH + 20:
                        self.rect.x = random.randrange(WIDTH - self.rect.width)
                        self.rect.y = random.randrange(-100, -40)
                        self.speedy = random.randrange(1, 3)

            class Enemy(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    self.image_orig = enemy_img
                    self.image_orig.set_colorkey(BLACK)
                    self.image = self.image_orig.copy()
                    self.rect = self.image.get_rect()
                    self.radius = int(self.rect.width * .85 / 2)
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-150, -100)
                    self.speedy = random.randrange(1, 3)
                    self.speedx = random.randrange(-1, 1)
                    self.rot = 0
                    self.rot_speed = random.randrange(-5, 5)
                    self.last_update = pygame.time.get_ticks()

                def update(self):
                    self.rect.x += self.speedx
                    self.rect.y += self.speedy
                    if self.rect.top > HEIGHT + 10 or \
                            self.rect.left < -25 or \
                            self.rect.right > WIDTH + 20:
                        self.rect.x = random.randrange(WIDTH - self.rect.width)
                        self.rect.y = random.randrange(-100, -40)
                        self.speedy = random.randrange(1, 3)

            class Bullet_enemy(pygame.sprite.Sprite):
                def __init__(self, x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = bullet_img
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.bottom = y
                    self.rect.centerx = x
                    self.speedy = 10

                def update(self):
                    self.rect.y += self.speedy
                    # убить, если он заходит за верхнюю часть экрана
                    if self.rect.bottom < 0:
                        self.kill()

            class Bullet(pygame.sprite.Sprite):
                def __init__(self, x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = bullet_img
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.bottom = y
                    self.rect.centerx = x
                    self.speedy = -10

                def update(self):
                    self.rect.y += self.speedy
                    # убиаем, если он заходит за верхнюю часть экрана
                    if self.rect.bottom < 0:
                        self.kill()

            class Animation(pygame.sprite.Sprite):
                def __init__(self, center, size):
                    pygame.sprite.Sprite.__init__(self)
                    self.size = size
                    self.image = anim[self.size][0]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.frame = 0
                    self.last_update = pygame.time.get_ticks()
                    self.frame_rate = 50

                def update(self):
                    now = pygame.time.get_ticks()
                    if now - self.last_update > self.frame_rate:
                        self.last_update = now
                        self.frame += 1
                        if self.frame == len(anim[self.size]):
                            self.kill()
                        else:
                            center = self.rect.center
                            self.image = anim[self.size][self.frame]
                            self.rect = self.image.get_rect()
                            self.rect.center = center

            all_sprites = pygame.sprite.Group()
            meteor = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Ship()
            all_sprites.add(player)
            star_list = []

            for i in range(10):
                m = Meteor()
                all_sprites.add(m)
                meteor.add(m)

            # Добавляем 2000 звезд со случайными координатами
            for i in range(2000):
                x = random.randrange(0, WIDTH)
                y = random.randrange(0, WIDTH)
                star_list.append([x, y, 2])
            clock = pygame.time.Clock()

            # Цикл игры
            running = True
            while running:
                # Ввод процесса (события)
                screen.fill(BLACK)
                for event in pygame.event.get():
                    # проверка для закрытия окна
                    if event.type == pygame.QUIT:
                        best_score.append(count_of_bullet)
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            hit_sound.play()
                            player.shoot()
                        if event.key == pygame.K_ESCAPE:
                            pausing = True
                            while pausing:
                                for event in pygame.event.get():
                                    # проверка для закрытия окна
                                    if event.type == pygame.QUIT:
                                        pausing = False
                                    elif event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_RETURN:
                                            pausing = False

                font = pygame.font.Font(None, 36)
                screen.blit(pygame.font.Font(None, 36)
                            .render("Health: {}%".format(count_of_life),
                                    1, (0, 180, 0)), (WIDTH - 200, 50))
                screen.blit(pygame.font.Font(None, 36)
                            .render("Score: {}".format(count_of_bullet),
                                    1, (0, 180, 0)), (WIDTH - 200, 100))
                # Обновление
                all_sprites.update()
                for star in star_list:
                    # Рисуем звезду
                    pygame.draw.circle(screen,
                                       colors[random.randint(0, 4)],
                                       star[0:2], 2)

                    # Смещаем звезду вниз
                    star[1] += star[2]

                    # Если звезда упала за низ окна
                    if star[1] > WIDTH:
                        # Устанавливаем для нее новые
                        # случайные координаты (конечноже выше экрана)
                        star[0] = random.randrange(0, WIDTH)
                        star[1] = random.randrange(-50, -10)

                hits = pygame.sprite.groupcollide(meteor, bullets, True, True)

                for hit in hits:
                    m = Meteor()
                    all_sprites.add(m)
                    meteor.add(m)
                    break_sound.play()
                    count_of_bullet += hit.radius // 2
                    all_sprites.add(Animation(hit.rect.center, 'lg'))
                    screen.blit(font.render("Score: {}".
                                            format(count_of_bullet), 1,
                                            (0, 180, 0)), (WIDTH - 200, 100))

                # Проверка, не ударил ли метеор игрока
                hits = pygame.sprite.spritecollide(player, meteor, False)
                for hit in hits:
                    count_of_life -= 1
                    screen.blit(font.render("Health: {}%".
                                            format(count_of_life), 1,
                                            (0, 180, 0)), (WIDTH - 200, 50))
                    all_sprites.add(Animation(hit.rect.center, 'sm'))
                    Break_falcon.play()
                    if count_of_life <= 0:
                        best_score.append(count_of_bullet)
                        self.flag_playing = False
                        running = False
                all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)
            pygame.quit()

    def Show_lvl2(self):
        self.flag_playing = True
        if self.flag_playing:
            import pygame
            import random
            from os import path

            def load_image(name, colorkey=None):
                fullname = path.join('data', name)
                if colorkey is not None:
                    image = pygame.image.load(fullname).convert()
                    if colorkey == -1:
                        colorkey = image.get_at((0, 0))
                    image.set_colorkey(colorkey)
                else:
                    image = pygame.image.load(fullname).convert_alpha()
                return image

            img_dir = path.join(path.dirname(__file__), 'sounds')

            size = WIDTH, HEIGHT = [1536, 864]
            screen = pygame.display.set_mode(size)
            FPS = 60
            x_pos = 1450
            y_pos = 50

            # Задаем цвета
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            colors = [(255, 255, 255), (0, 0, 255),
                      (30, 144, 255), (255, 69, 0),
                      (255, 255, 0)]
            count_of_life = 100
            count_of_bullet = 0
            # Создаем игру и окно
            pygame.init()
            pygame.mixer.init()
            pygame.display.set_caption("STAR BATTLE")
            clock = pygame.time.Clock()
            sounds = path.join(path.dirname(__file__), 'sounds')

            class Ship(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    self.shield = 100
                    self.image = pygame.transform.scale(player_img, (130, 100))
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.centerx = WIDTH / 2
                    self.rect.bottom = HEIGHT - 10
                    self.speedx = 0

                def update(self):
                    self.speedx = 0
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_LEFT]:
                        self.speedx = -5
                    if keystate[pygame.K_RIGHT]:
                        self.speedx = 5
                    self.rect.x += self.speedx
                    if self.rect.right > WIDTH:
                        self.rect.right = WIDTH
                    if self.rect.left < 0:
                        self.rect.left = 0

                def shoot(self):
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

            class Meteor(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    meteor_list = ['meteor.png', 'meteor2.png', 'meteor4.png']
                    self.image_orig = \
                        load_image(meteor_list[random.randint(0, 2)])
                    self.image_orig.set_colorkey(BLACK)
                    self.image = self.image_orig.copy()
                    self.rect = self.image.get_rect()
                    self.radius = int(self.rect.width * .85 / 2)
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-150, -100)
                    self.speedy = random.randrange(1, 8)
                    self.speedx = random.randrange(-3, 3)
                    self.rot = 0
                    self.rot_speed = random.randrange(-8, 8)
                    self.last_update = pygame.time.get_ticks()

                def update(self):
                    self.rect.x += self.speedx
                    self.rect.y += self.speedy
                    if self.rect.top > HEIGHT + 10 \
                            or self.rect.left < -25 or \
                            self.rect.right > WIDTH + 20:
                        self.rect.x = random.randrange(WIDTH - self.rect.width)
                        self.rect.y = random.randrange(-100, -40)
                        self.speedy = random.randrange(1, 8)

            class Bullet(pygame.sprite.Sprite):
                def __init__(self, x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = bullet_img
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.bottom = y
                    self.rect.centerx = x
                    self.speedy = -10

                def update(self):
                    self.rect.y += self.speedy
                    # убить, если он заходит за верхнюю часть экрана
                    if self.rect.bottom < 0:
                        self.kill()

            class Animation(pygame.sprite.Sprite):
                def __init__(self, center, size):
                    pygame.sprite.Sprite.__init__(self)
                    self.size = size
                    self.image = anim[self.size][0]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.frame = 0
                    self.last_update = pygame.time.get_ticks()
                    self.frame_rate = 50

                def update(self):
                    now = pygame.time.get_ticks()
                    if now - self.last_update > self.frame_rate:
                        self.last_update = now
                        self.frame += 1
                        if self.frame == len(anim[self.size]):
                            self.kill()
                        else:
                            center = self.rect.center
                            self.image = anim[self.size][self.frame]
                            self.rect = self.image.get_rect()
                            self.rect.center = center
                            screen.blit(font.
                                        render('+ {}'.
                                               format(count_of_bullet),
                                               1, (0, 0, 0)), self.rect)

            def paused():
                pausing = True
                while pausing:
                    for event in pygame.event.get():
                        # проверка для закрытия окна
                        if event.type == pygame.QUIT:
                            pausing = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                pausing = False

            # Загрузка всей игровой графики
            player_img = load_image("Ship_of_skywalker.png")
            meteor_img = load_image("meteor.png")
            bullet_img = load_image("shot_luke.png")
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            # Загрузка всех звуков
            hit_sound = pygame.mixer.Sound(path.join(sounds, 'hit.wav'))
            break_sound = pygame.mixer.Sound(path.join(sounds, 'break.wav'))
            fly_sound = pygame.mixer.Sound(path.join(sounds, 'fly.wav'))
            Order66 = pygame.mixer.Sound(path.join(sounds, 'Order-66.wav'))
            Break_falcon = \
                pygame.mixer.Sound(path.join(sounds, 'break_falcon.wav'))
            anim = {'lg': [], 'sm': []}

            for j in range(4):
                for i in range(8):
                    img = load_image('explosions.png')
                    rect = pygame.Rect(0, 0, img.get_width() // 8,
                                       img.get_height() // 4)
                    anim['lg'].append(img.subsurface(pygame.Rect(
                        (rect.w * i, rect.h * j), rect.size)))
                    anim['sm'].append(img.subsurface(pygame.Rect(
                        (rect.w * i, rect.h * j), rect.size)))

            all_sprites = pygame.sprite.Group()
            meteor = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Ship()
            all_sprites.add(player)
            star_list = []

            for i in range(20):
                m = Meteor()
                all_sprites.add(m)
                meteor.add(m)

            # Добавляем 1000 звезд со случайными координатами
            for i in range(2000):
                x = random.randrange(0, WIDTH)
                y = random.randrange(0, WIDTH)
                star_list.append([x, y, 2])
            clock = pygame.time.Clock()

            # Цикл игры
            running = True
            while running:
                # Ввод процесса (события)
                screen.fill(BLACK)
                for event in pygame.event.get():
                    # проверка для закрытия окна
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            hit_sound.play()
                            player.shoot()
                        if event.key == pygame.K_ESCAPE:
                            paused()

                font = pygame.font.Font(None, 36)
                screen.blit(pygame.font.Font(None, 36)
                            .render("Health: {}%".format(count_of_life),
                                    1, (0, 180, 0)), (WIDTH - 200, 50))
                screen.blit(pygame.font.Font(None, 36)
                            .render("Score: {}".format(count_of_bullet),
                                    1, (0, 180, 0)), (WIDTH - 200, 100))
                # Обновление
                all_sprites.update()
                for star in star_list:
                    # Рисуем звезду
                    pygame.draw.circle(screen,
                                       colors[random.randint(0, 4)],
                                       star[0:2], 2)

                    # Смещаем звезду вниз
                    star[1] += star[2]

                    # Если звезда упала за низ окна
                    if star[1] > WIDTH:
                        # Устанавливаем для нее новые
                        # случайные координаты (конечноже выше экрана)
                        star[0] = random.randrange(0, WIDTH)
                        star[1] = random.randrange(-50, -10)

                hits = pygame.sprite.groupcollide(meteor, bullets, True, True)

                for hit in hits:
                    m = Meteor()
                    all_sprites.add(m)
                    meteor.add(m)
                    break_sound.play()
                    count_of_bullet += hit.radius // 2
                    all_sprites.add(Animation(hit.rect.center, 'lg'))
                    screen.blit(font.render("Score: {}".
                                            format(count_of_bullet),
                                            1, (0, 180, 0)),
                                (WIDTH - 200, 100))

                # Проверка, не ударил ли метеор игрока
                hits = pygame.sprite.spritecollide(player, meteor, False)
                for hit in hits:
                    count_of_life -= 1
                    screen.blit(font.render("Health: {}%".
                                            format(count_of_life),
                                            1, (0, 180, 0)),
                                (WIDTH - 200, 50))
                    player.shield -= hit.radius * 2
                    all_sprites.add(Animation(hit.rect.center, 'sm'))
                    Break_falcon.play()
                    if count_of_life <= 0:
                        best_score.append(count_of_bullet)
                        self.flag_playing = False
                        running = False
                # Выводим на экран все что нарисовали
                all_sprites.draw(screen)
                # После отрисовки всего, переворачиваем экран
                pygame.display.flip()
                clock.tick(FPS)
            pygame.quit()

    def Show_lvl3(self):
        if self.flag_playing:
            import pygame
            import random
            from os import path

            def load_image(name, colorkey=None):
                fullname = path.join('data', name)
                if colorkey is not None:
                    image = pygame.image.load(fullname).convert()
                    if colorkey == -1:
                        colorkey = image.get_at((0, 0))
                    image.set_colorkey(colorkey)
                else:
                    image = pygame.image.load(fullname).convert_alpha()
                return image

            img_dir = path.join(path.dirname(__file__), 'sounds')

            size = WIDTH, HEIGHT = [1536, 864]
            screen = pygame.display.set_mode(size)
            FPS = 60
            x_pos = 1450
            y_pos = 50

            # Задаем цвета
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            colors = [(255, 255, 255), (0, 0, 255),
                      (30, 144, 255), (255, 69, 0),
                      (255, 255, 0)]
            count_of_life = 100
            count_of_bullet = 0
            # Создаем игру и окно
            pygame.init()
            pygame.mixer.init()
            pygame.display.set_caption("STAR BATTLE")
            clock = pygame.time.Clock()
            sounds = path.join(path.dirname(__file__), 'sounds')

            class Ship(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    self.shield = 100
                    self.image = pygame.transform.scale(player_img, (120, 90))
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.centerx = WIDTH / 2
                    self.rect.bottom = HEIGHT - 10
                    self.speedx = 0

                def update(self):
                    self.speedx = 0
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_LEFT]:
                        self.speedx = -5
                    if keystate[pygame.K_RIGHT]:
                        self.speedx = 5
                    self.rect.x += self.speedx
                    if self.rect.right > WIDTH:
                        self.rect.right = WIDTH
                    if self.rect.left < 0:
                        self.rect.left = 0

                def shoot(self):
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

            class Meteor(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    meteor_list = ['meteor.png',
                                   'meteor2.png',
                                   'meteor3.png',
                                   'meteor4.png']
                    self.image_orig = \
                        load_image(meteor_list[random.randint(0, 3)])
                    self.image_orig.set_colorkey(BLACK)
                    self.image = self.image_orig.copy()
                    self.rect = self.image.get_rect()
                    self.radius = int(self.rect.width * .85 / 2)
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-150, -100)
                    self.speedy = random.randrange(1, 8)
                    self.speedx = random.randrange(-3, 3)
                    self.rot = 0
                    self.rot_speed = random.randrange(-8, 8)
                    self.last_update = pygame.time.get_ticks()

                def update(self):
                    self.rect.x += self.speedx
                    self.rect.y += self.speedy
                    if self.rect.top > HEIGHT + 10 or \
                            self.rect.left < -25 or \
                            self.rect.right > WIDTH + 20:
                        self.rect.x = random.randrange(WIDTH - self.rect.width)
                        self.rect.y = random.randrange(-100, -40)
                        self.speedy = random.randrange(1, 15)

            class Bullet(pygame.sprite.Sprite):
                def __init__(self, x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = bullet_img
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.bottom = y
                    self.rect.centerx = x
                    self.speedy = -10

                def update(self):
                    self.rect.y += self.speedy
                    # убить, если он заходит за верхнюю часть экрана
                    if self.rect.bottom < 0:
                        self.kill()

            class Animation(pygame.sprite.Sprite):
                def __init__(self, center, size):
                    pygame.sprite.Sprite.__init__(self)
                    self.size = size
                    self.image = explosion_anim[self.size][0]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.frame = 0
                    self.last_update = pygame.time.get_ticks()
                    self.frame_rate = 50

                def update(self):
                    now = pygame.time.get_ticks()
                    if now - self.last_update > self.frame_rate:
                        self.last_update = now
                        self.frame += 1
                        if self.frame == len(explosion_anim[self.size]):
                            self.kill()
                        else:
                            center = self.rect.center
                            self.image = explosion_anim[self.size][self.frame]
                            self.rect = self.image.get_rect()
                            self.rect.center = center
                            screen.blit(font.
                                        render('+ {}'.format(count_of_bullet),
                                               1, (0, 0, 0)), self.rect)

            def paused():
                pausing = True
                while pausing:
                    for event in pygame.event.get():
                        # проверка для закрытия окна
                        if event.type == pygame.QUIT:
                            pausing = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                pausing = False

            # Загрузка всей игровой графики
            player_img = load_image("Ship_of_dard_mall.png")
            meteor_img = load_image("meteor.png")
            bullet_img = load_image("shot_mall.png")
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            # Загрузка всех звуков
            hit_sound = pygame.mixer.Sound(path.join(sounds, 'hit.wav'))
            break_sound = pygame.mixer.Sound(path.join(sounds, 'break.wav'))
            fly_sound = pygame.mixer.Sound(path.join(sounds, 'fly.wav'))
            Order66 = pygame.mixer.Sound(path.join(sounds, 'Order-66.wav'))
            Break_falcon = pygame.mixer.\
                Sound(path.join(sounds, 'break_falcon.wav'))
            explosion_anim = {'lg': [], 'sm': []}

            for j in range(4):
                for i in range(8):
                    img = load_image('explosions.png')
                    rect = pygame.Rect(0, 0, img.get_width() // 8,
                                       img.get_height() // 4)
                    explosion_anim['lg'].append(img.subsurface(pygame.Rect(
                        (rect.w * i, rect.h * j), rect.size)))
                    explosion_anim['sm'].append(img.subsurface(pygame.Rect(
                        (rect.w * i, rect.h * j), rect.size)))

            all_sprites = pygame.sprite.Group()
            meteor = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Ship()
            all_sprites.add(player)
            star_list = []

            for i in range(30):
                m = Meteor()
                all_sprites.add(m)
                meteor.add(m)

            # Добавляем 1000 звезд со случайными координатами
            for i in range(2000):
                x = random.randrange(0, WIDTH)
                y = random.randrange(0, WIDTH)
                star_list.append([x, y, 2])
            clock = pygame.time.Clock()

            # Цикл игры
            running = True
            while running:
                # Ввод процесса (события)
                screen.fill(BLACK)
                for event in pygame.event.get():
                    # проверка для закрытия окна
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            hit_sound.play()
                            player.shoot()
                        if event.key == pygame.K_ESCAPE:
                            paused()

                font = pygame.font.Font(None, 36)
                screen.blit(pygame.font.Font(None, 36)
                            .render("Health: {}%".format(count_of_life),
                                    1, (0, 180, 0)), (WIDTH - 200, 50))
                screen.blit(pygame.font.Font(None, 36)
                            .render("Score: {}".format(count_of_bullet),
                                    1, (0, 180, 0)), (WIDTH - 200, 100))
                # Обновление
                all_sprites.update()
                for star in star_list:
                    # Рисуем звезду
                    pygame.draw.circle(screen,
                                       colors[random.randint(0, 4)],
                                       star[0:2], 2)

                    # Смещаем звезду вниз
                    star[1] += star[2]

                    # Если звезда упала за низ окна
                    if star[1] > WIDTH:
                        # Устанавливаем для нее новые
                        # случайные координаты (конечноже выше экрана)
                        star[0] = random.randrange(0, WIDTH)
                        star[1] = random.randrange(-50, -10)

                hits = pygame.sprite.groupcollide(meteor, bullets, True, True)

                for hit in hits:
                    m = Meteor()
                    all_sprites.add(m)
                    meteor.add(m)
                    break_sound.play()
                    count_of_bullet += hit.radius // 2
                    all_sprites.add(Animation(hit.rect.center, 'lg'))
                    screen.blit(font.render("Score: {}".
                                            format(count_of_bullet),
                                            1, (0, 180, 0)),
                                (WIDTH - 200, 100))

                # Проверка, не ударил ли метеор игрока
                hits = pygame.sprite.spritecollide(player, meteor, False)
                for hit in hits:
                    count_of_life -= 1
                    screen.blit(font.render("Health: {}%".
                                            format(count_of_life),
                                            1, (0, 180, 0)), (WIDTH - 200, 50))
                    all_sprites.add(Animation(hit.rect.center, 'sm'))
                    Break_falcon.play()
                    if count_of_life <= 0:
                        screen.fill(BLACK)
                        self.flag_playing = False
                        running = False
                # Выводим на экран все что нарисовали
                all_sprites.draw(screen)
                # После отрисовки всего, переворачиваем экран
                pygame.display.flip()
                clock.tick(FPS)
            pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())
