import pygame
import os

# Функции для отрисовки кнопок и обработки событий в меню

def draw_button_menu(screen, button_rect, text, hover=False):
    """Рисует кнопку на экране."""
    button_color = (106, 209, 19)  # зеленый цвет фона
    border_color = (94, 194, 23)  # зеленый цвет границы
    text_color = (0, 0, 0)  # черный цвет текста

    if hover:
        button_color = (22, 115, 181)  # синий цвет фона при наведении
        border_color = (34, 132, 201)  # синий цвет границы при наведении
        text_color = (255, 255, 255)  # белый цвет текста

    # Рисуем границу кнопки
    pygame.draw.rect(screen, border_color, button_rect)
    # Рисуем кнопку внутри границы
    pygame.draw.rect(screen, button_color, button_rect.inflate(-6, -6))

    # Отрисовка текста
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def check_hover(button_rect, mouse_pos):
    """Проверяет, находится ли указатель мыши над кнопкой."""
    return button_rect.collidepoint(mouse_pos)

def draw_menu(screen, buttons, background_image):
    """Отрисовка стартового меню с фоном."""
    screen.blit(background_image, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    for key, rect in buttons.items():
        draw_button_menu(screen, rect, key.replace("_", " ").title(), check_hover(rect, mouse_pos))

def create_buttons(screen_width, screen_height):
    """Создание кнопок меню."""
    buttons = {
        "Старт игры": pygame.Rect(screen_width // 2 - 100, screen_height // 3 - 75, 200, 50),
        "Настройки": pygame.Rect(screen_width // 2 - 100, screen_height // 3 + 25, 200, 50),  # Новая кнопка "Настройки"
        "Правила": pygame.Rect(screen_width // 2 - 100, screen_height // 3 + 125, 200, 50),
        "Выход из игры": pygame.Rect(screen_width // 2 - 100, screen_height * 2 // 3 - 25, 200, 50),
        "О разработчике": pygame.Rect(screen_width - 250, screen_height - 75, 200, 50)
    }
    return buttons

def handle_menu_click(position, buttons):
    """Обрабатывает клики по кнопкам меню."""
    for key, rect in buttons.items():
        if rect.collidepoint(position):
            return key
    return None

# Загрузка фонового экрана
def load_background_image(filename):
    """Загрузка фонового изображения по указанному имени файла."""
    current_dir = os.path.dirname(__file__)  # Получаем директорию текущего файла
    image_path = os.path.join(current_dir, 'pictures', filename)  # Формируем путь к изображению
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {filename}:", e)
        return pygame.Surface((0, 0))  # Пустая поверхность в случае ошибки
    
# Загрузка музыки
def load_background_music():
    """Загружает и воспроизводит фоновую музыку."""
    current_dir = os.path.dirname(__file__)  # Получаем директорию текущего файла
    music_path = os.path.join(current_dir, 'music', 'menu.mp3')  # Укажите имя вашего музыкального файла
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # Воспроизведение музыки в бесконечном цикле
    except pygame.error as e:
        print("Ошибка загрузки музыкального файла:", e)

def load_text_from_file(filename):
    """Функция для загрузки текста из файла в папке 'texts'."""
    current_dir = os.path.dirname(__file__)  # Получаем директорию текущего файла
    file_path = os.path.join(current_dir, 'texts', filename)  # Формируем путь к файлу в папке 'texts'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return ""

# Функции для отрисовки и обработки событий на экранах "Правила" и "О разработчике"

def draw_rules_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, mouse_pos, rules_text_filename):
    """Отрисовка экрана с правилами игры."""
    rules_text = load_text_from_file(rules_text_filename)  # Загружаем текст из файла

    # Создаем объект шрифта
    font = pygame.font.Font(None, 36)

    # Разбиваем текст на отдельные строки
    lines = rules_text.split('\n')

    # Координаты начала первой колонки
    x_pos = 135
    y_pos = 100

    # Отрисовываем строки
    for i, line in enumerate(lines):
        if i == 0:  # Первая строка жирным шрифтом
            font.set_bold(True)
            text_surface = font.render(line, True, (0, 0, 0))
            font.set_bold(False)  # Возвращаем шрифт к обычному после первой строки
        else:
            text_surface = font.render(line, True, (0, 0, 0))

        text_rect = text_surface.get_rect(left=x_pos, top=y_pos)

        # Переход на вторую колонку после 10 строк
        if i == 12:
            x_pos = SCREEN_WIDTH // 2  # Начало второй колонки по центру экрана
            y_pos = 100  # Возвращаемся к начальной высоте

        y_pos += text_surface.get_height() + 10  # Сдвигаем каждую следующую строку вниз

        screen.blit(text_surface, text_rect)

    # Кнопка "Вернуться"
    return_button = pygame.Rect(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 60, 200, 50)
    draw_button_menu(screen, return_button, "Вернуться", check_hover(return_button, mouse_pos))
    return return_button

def draw_about_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, mouse_pos, text_y_pos, about_text_filename):
    """Отрисовка экрана 'О разработчике' с анимацией текста."""
    about_text = load_text_from_file(about_text_filename)  # Загружаем текст из файла

    # Создаем два объекта шрифта: обычный и жирный
    regular_font = pygame.font.Font(None, 36)
    bold_font = pygame.font.Font(None, 36)
    bold_font.set_bold(True)  # Устанавливаем жирный шрифт

    # Разбиваем текст на отдельные строки
    lines = about_text.split('\n')

    # Отрисовываем каждую строку
    for i, line in enumerate(lines):
        # Для первой строки используем жирный шрифт
        if i == 0:
            font = bold_font
        else:
            font = regular_font

        text_surface = font.render(line, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, text_y_pos + i * 40))  # Сдвигаем каждую следующую строку вниз
        screen.blit(text_surface, text_rect)

    # Кнопка "Вернуться"
    return_button = pygame.Rect(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 60, 200, 50)
    draw_button_menu(screen, return_button, "Вернуться", check_hover(return_button, mouse_pos))
    return return_button

def draw_slider(screen, slider_rect, handle_rect, value):
    """Отрисовка ползунка для регулировки громкости."""
    # Рисуем трек слайдера
    pygame.draw.rect(screen, (200, 200, 200), slider_rect)
    
    # Обводим слайдер черным контуром
    pygame.draw.rect(screen, (0, 0, 0), slider_rect, 2)
    
    # Рисуем активную часть слайдера (зеленый)
    active_width = int(slider_rect.width * value)
    active_rect = pygame.Rect(slider_rect.left, slider_rect.top, active_width, slider_rect.height)
    pygame.draw.rect(screen, (0, 255, 0), active_rect)
    
    # Вычисляем x позицию ручки, ограниченную шириной слайдера
    handle_x = slider_rect.left + active_width - handle_rect.width // 2
    
    # Ограничиваем положение ползунка границами слайдера
    handle_x = max(slider_rect.left + handle_rect.width // 2, min(slider_rect.right - handle_rect.width // 2, handle_x))
    
    # Рисуем ручку слайдера как квадрат красного цвета
    handle_rect.centerx = handle_x
    handle_rect.centery = slider_rect.centery
    pygame.draw.rect(screen, (255, 0, 0), handle_rect)

def draw_settings_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, mouse_pos, slider_value, background_image):
    """Отрисовка экрана настроек."""
    # Отрисовка фонового изображения
    screen.blit(background_image, (0, 0))
    
    # Настройка шрифта и отрисовка надписи "Уровень звука"
    font = pygame.font.Font(None, 36)
    volume_label = font.render("Уровень звука", True, (0, 0, 0))
    label_rect = volume_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(volume_label, label_rect)
    
    # Рисуем ползунок громкости с уменьшенной длиной
    slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 20)  # Длина 200 вместо SCREEN_WIDTH // 2
    handle_rect = pygame.Rect(0, 0, 20, 30)  # Уменьшенный размер ручки
    draw_slider(screen, slider_rect, handle_rect, slider_value)
    
    # Кнопка "Вернуться"
    return_button = pygame.Rect(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 60, 200, 50)
    draw_button_menu(screen, return_button, "Вернуться", check_hover(return_button, mouse_pos))

# # Временный исполняемый код для тестирования
# if __name__ == "__main__":
#     pygame.init()
#     pygame.mixer.init()  # Инициализация микшера

#     infoObject = pygame.display.Info()
#     SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
#     pygame.display.set_caption("Тестовое меню")

#     background_image = load_background_image()
#     load_background_music()  # Загрузка и воспроизведение музыки
#     buttons = create_buttons(SCREEN_WIDTH, SCREEN_HEIGHT)

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 response = handle_menu_click(event.pos, buttons)
#                 if response == "start_game":
#                     print("Начало игры")
#                 elif response == "settings":
#                     print("Настройки")
#                 elif response == "rules":
#                     print("Правила")
#                 elif response == "exit":
#                     running = False
#                 elif response == "about":
#                     print("О разработчике")

#         draw_menu(screen, buttons, background_image)
#         pygame.display.flip()

#     pygame.quit()