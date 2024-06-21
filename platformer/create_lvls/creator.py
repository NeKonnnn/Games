import pygame
import button
import csv
import pickle
from settings_creator import *

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Редактор Уровней')

# Определение игровых переменных
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0

# Загрузка изображений тайлов
TILE_TYPES = 50  # Установите нужное количество тайлов здесь
img_list = []
for x in range(TILE_TYPES):
    try:
        img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
    except FileNotFoundError:
        continue  # Пропускаем отсутствующие файлы
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()

# Определение шрифта и создание пустого списка тайлов
font = pygame.font.SysFont('Futura', 30)
world_data = [[-1] * MAX_COLS for _ in range(ROWS)]

# Функция для отображения текста
def draw_text(text, font, text_col, x, y):
    """Отображение текста на экране."""
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Функция для отрисовки фона
def draw_bg():
    """Заливка экрана серым цветом."""
    screen.fill((128, 128, 128))

# Функция для отрисовки сетки
def draw_grid():
    """Отрисовка сетки на экране."""
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

# Функция для отрисовки мира
def draw_world():
    """Отрисовка тайлов на экране."""
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# Создание кнопок
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

# Автоматическое создание списка кнопок тайлов
button_list = []
button_col, button_row = 0, 0
for i, img in enumerate(img_list):
    # Вычисляем позицию для каждой кнопки
    x_pos = SCREEN_WIDTH + BUTTON_PADDING + (button_col * (BUTTON_SIZE[0] + BUTTON_PADDING))
    y_pos = BUTTON_PADDING + (button_row * (BUTTON_SIZE[1] + BUTTON_PADDING))

    tile_button = button.Button(x_pos, y_pos, img, 1)
    button_list.append(tile_button)

    button_row += 1
    if button_row == BUTTONS_PER_ROW:
        button_row = 0
        button_col += 1

# Основной игровой цикл
run = True
while run:
    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Уровень: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text(f'Длина карты: {MAX_COLS}, Ширина карты: {ROWS}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 120)
    draw_text('Нажмите ВВЕРХ или ВНИЗ для смены уровня', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # Изменение цвета фона справа на панели на белый
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # Сохранение и загрузка данных
    if save_button.draw(screen):
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # Управление скроллингом карты
    if scroll_left and scroll > 0:
        scroll -= 5 * SCROLL_SPEED
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * SCROLL_SPEED

    # Обработка нажатий мыши и клавиатуры
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                SCROLL_SPEED = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                SCROLL_SPEED = 1

    pygame.display.update()

pygame.quit()