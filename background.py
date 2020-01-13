import pygame
import random

# Инициализируем pygame
pygame.init()

black = [0, 0, 0]
white = [255, 255, 255]

# Задаем размеры окна
size = [1536, 864]
screen = pygame.display.set_mode(size)

# Устанавливаем заголовок
pygame.display.set_caption("Star Animation")

# Создаем пустой массив
star_list = []

# Добавляем 50 звезд со случайными координатами
for i in range(1000):
    x = random.randrange(0, 1536)
    y = random.randrange(0, 1536)
    speed = random.randint(1, 3)
    star_list.append([x, y, speed])

clock = pygame.time.Clock()

# Повторяем цикл, пока пользователь не закроет окно
running = True


while running:

    for event in pygame.event.get():  # Проходим по всем событиям
        if event.type == pygame.QUIT:  # Если пользователь закрыд окно
            running = False  # Помечаем что пора заканчивать

    # Очищаем окно
    screen.fill(black)

    # Обрабатываем каждую звезду в списке
    for star in star_list:
        # Рисуем звезду
        pygame.draw.circle(screen, white, star[0:2], 2)

        # Смещаем звезду вниз
        star[1] += star[2]

        # Если звезда упала за низ окна
        if star[1] > 1536:
            # Устанавливаем для нее новые случайные координаты (конечноже выше экрана)
            star[0] = random.randrange(0, 1536)
            star[1] = random.randrange(-50, -10)
    # Выводим на экран все что нарисовали
    pygame.display.flip()
    clock.tick(60)

pygame.quit()