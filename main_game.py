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
        # Оставляем картинку прозрачной
        image = pygame.image.load(fullname).convert_alpha()
    return image


img_dir = path.join(path.dirname(__file__), 'data')
size = WIDTH, HEIGHT = [1536, 500]
screen = pygame.display.set_mode(size)
FPS = 60
x_pos = 1450
y_pos = 50

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colors = [(255, 255, 255), (0, 0, 255), (30, 144, 255), (255, 69, 0), (255, 255, 0)]
count_of_life = 100
count_of_bullet = 0
# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("STAR BATTLE")
clock = pygame.time.Clock()
snd_dir = path.join(path.dirname(__file__), 'data')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shield = 100
        self.image = pygame.transform.scale(player_img, (50, 38))
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


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        meteor_list = ['meteor.png', 'meteor2.png', 'meteor4.png']
        n = random.randint(0, 2)
        self.image_orig = load_image(meteor_list[n])
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

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, center):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.rect.center = center
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(self.rect.x, -1 * self.rect.y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# Загрузка всей игровой графики
player_img = load_image("falcon.png")
meteor_img = load_image("meteor.png")
bullet_img = load_image("laser.png")
hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit.wav'))
break_sound = pygame.mixer.Sound(path.join(snd_dir, 'break.wav'))
fly_sound = pygame.mixer.Sound(path.join(snd_dir, 'fly.wav'))
Order66 = pygame.mixer.Sound(path.join(snd_dir, 'Order-66.wav'))


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
star_list = []

for i in range(15):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Добавляем 1000 звезд со случайными координатами
for i in range(1000):
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
    font = pygame.font.Font(None, 36)
    text = font.render("Life: {}".format(count_of_life), 1, (0, 180, 0))
    screen.blit(text, (1400, 50))
    text2 = font.render("Hits: {}".format(count_of_bullet), 1, (0, 180, 0))
    screen.blit(text2, (1400, 100))
    # Обновление
    all_sprites.update()
    for star in star_list:
        # Рисуем звезду
        number = random.randint(0, 4)
        pygame.draw.circle(screen, colors[number], star[0:2], 2)

        # Смещаем звезду вниз
        star[1] += star[2]

        # Если звезда упала за низ окна
        if star[1] > WIDTH:
            # Устанавливаем для нее новые случайные координаты (конечноже выше экрана)
            star[0] = random.randrange(0, WIDTH)
            star[1] = random.randrange(-50, -10)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        break_sound.play()
        count_of_bullet += 1
        all_sprites.add(AnimatedSprite(load_image("explosions.png"), 8, 4, hit.rect.center))
        print(m.rect.x, -1 * m.rect.y)
        text2 = font.render("Hits: {}".format(count_of_bullet), 1, (0, 180, 0))
        screen.blit(text2, (WIDTH - 136, 100))

    # Проверка, не ударил ли метеор игрока
    hits = pygame.sprite.spritecollide(player, mobs, False)
    for hit in hits:
        count_of_life -= 1
        text = font.render("Life: {}".format(count_of_life), 1, (0, 180, 0))
        screen.blit(text, (WIDTH - 136, 50))
        player.shield -= hit.radius * 2
        if count_of_life <= 0:
            running = False
    # Выводим на экран все что нарисовали
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()