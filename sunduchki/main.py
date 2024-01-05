import pygame
import random
import os
import time
from menu import *

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Инициализация микшера

# Получение информации о дисплее
infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h

# Создание окна с размерами, соответствующими разрешению экрана пользователя
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Сундучки")

# Константы
CARD_WIDTH, CARD_HEIGHT = 147, 214  # Предполагаемые размеры карты

# Переменные для управления ходом
player_turn_continues = False
# Инициализация списка для хранения всех сообщений диалога
all_dialog_messages = []

requested_card = None

# Инициализация счетчиков сундучков
player_chests_collected = 0
computer_chests_collected = 0


# Константы для интерфейса
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT = 400, 150
CHEST_SIZE = 147  # Размеры сундуков

# Шрифт для текста
button_font = pygame.font.Font(None, 36)

# Загрузка ресурсов
def load_image(name, directory='new_cards'):
    """Загрузка изображения."""
    path = os.path.join(directory, name)
    return pygame.image.load(path).convert_alpha()

# Загрузка карт, сундуков и фона
card_images = {f'{rank}{suit}': load_image(f'{rank}{suit}.jpg') 
               for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] 
               for suit in ['c', 'p', 'b', 'k']}
back_card_image = load_image('rubashka.jpg')
background_image = load_image('stol.jpg', directory='.')
chest_p_image = load_image('chest_p.jpg', directory='.')
chest_c_image = load_image('chest_c.jpg', directory='.')

class Card:
    """Класс для представления карты."""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.image = card_images[f'{rank}{suit}']

class Deck:
    """Класс колоды карт."""
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] 
                      for suit in ['c', 'p', 'b', 'k']]
        random.shuffle(self.cards)

    def draw_card(self):
        """Извлечение карты из колоды."""
        return self.cards.pop() if self.cards else None

class Player:
    """Класс игрока."""
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
        self.hand = []

    def draw_cards(self, deck, count=1):
        """Взять карты из колоды."""
        for _ in range(count):
            card = deck.draw_card()
            if card:
                self.hand.append(card)
                
# Функция для отрисовки кнопки
def draw_button():
    button_text = button_font.render('Нет такой карты', True, (0, 0, 0))
    button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 20, SCREEN_HEIGHT - CARD_HEIGHT - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, (255, 0, 0), button_rect)  # Ярко-красный фон кнопки для визуализации
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))
    return button_rect

# Функция для всех диалогов
def draw_container_button():
    container_button_text = button_font.render('Контейнер', True, (0, 0, 0))
    container_button_rect = pygame.Rect(20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), container_button_rect)
    screen.blit(container_button_text, (container_button_rect.x + 10, container_button_rect.y + 10))
    print("Рисуется кнопка 'Нет такой карты'")
    return container_button_rect

# Функция для отрисовки диалогового окна
def draw_dialog_box(messages):
    dialog_y_pos = (SCREEN_HEIGHT - DIALOG_BOX_HEIGHT) // 2
    dialog_rect = pygame.Rect(20, dialog_y_pos, DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), dialog_rect)  # Белый фон окна
    if messages:
        last_message = messages[-1]
        text = button_font.render(last_message, True, (0, 0, 0))
        screen.blit(text, (dialog_rect.x + 10, dialog_rect.y + 10))

# Функция для отрисовки сундуков
def draw_chests():
    # Отрисовка сундука игрока (снизу)
    screen.blit(chest_p_image, (SCREEN_WIDTH - CHEST_SIZE - 20, SCREEN_HEIGHT - CHEST_SIZE - 10))

    # Отрисовка сундука компьютера (сверху)
    screen.blit(chest_c_image, (SCREEN_WIDTH - CHEST_SIZE - 20, 10))
                
# Функция для группировки карт по номиналам
def group_cards_by_rank(hand):
    grouped = {}
    for card in hand:
        if card.rank in grouped:
            grouped[card.rank].append(card)
        else:
            grouped[card.rank] = [card]
    return grouped

# Функция для рисования групп карт
def draw_card_group(group, start_x, y_pos, overlap=30):
    for i, card in enumerate(group):
        card_x_pos = start_x + i * overlap
        card_y_pos = y_pos
        screen.blit(card.image, (card_x_pos, card_y_pos))
        if i == len(group) - 1:  # Последняя карта в группе
            return (card_x_pos, card_y_pos)

def load_game_music():
    """Загружает и воспроизводит фоновую музыку для игры."""
    current_dir = os.path.dirname(__file__)  # Получаем директорию текущего файла
    music_path = os.path.join(current_dir, 'music', 'game.mp3')  # Путь к файлу музыки игры
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # Воспроизведение музыки в бесконечном цикле
    except pygame.error as e:
        print("Ошибка загрузки музыкального файла:", e)

# Обновленная функция для отображения карт игрока и противника
def draw_hand(hand, y_pos, is_player):
    grouped_hand = group_cards_by_rank(hand)
    start_x = (SCREEN_WIDTH - (len(grouped_hand) * (CARD_WIDTH + 30) - 30)) // 2
    for group in grouped_hand.values():
        draw_card_group(group, start_x, y_pos)
        start_x += CARD_WIDTH + 10

# Функции для игровой логики
# Функции для игровой логики
def deal_cards(deck, players, card_count=7):
    """Раздача карт игрокам."""
    for player in players:
        player.draw_cards(deck, card_count)
    print("Карты разданы")

def card_clicked(cards, x, y):
    """Определение, кликнул ли игрок на карту."""
    for i, group in enumerate(group_cards_by_rank(cards).values()):
        card_x_pos, card_y_pos = draw_card_group(group, calculate_start_x(i), SCREEN_HEIGHT - CARD_HEIGHT - 10, overlap=30)
        card_rect = pygame.Rect(card_x_pos, card_y_pos, CARD_WIDTH, CARD_HEIGHT)
        if card_rect.collidepoint(x, y):
            print(f"Кликнута карта: {group[0]}")
            return group[0]  # Возвращаем первую карту в группе
    print("Карта не выбрана")
    return None

def calculate_start_x(group_index):
    """Рассчитать начальную X позицию группы карт."""
    start_x = (SCREEN_WIDTH - (len(group_cards_by_rank(players[0].hand)) * (CARD_WIDTH + 30) - 30)) // 2 + group_index * (CARD_WIDTH + 10)
    print(f"Начальная X позиция группы {group_index}: {start_x}")
    return start_x

# Ход человека
def player_turn(card, player_hand, opponent_hand, dialog_messages):
    """Обработка хода игрока."""
    global player_turn_continues
    print(">>> player_turn called, current_turn:", current_turn)
    check_full_set(player_hand, dialog_messages, is_player=True)

    if card.rank in [c.rank for c in opponent_hand]:
        # У компьютера есть карта, отдать все карты этого номинала
        cards_to_give = [c for c in opponent_hand if c.rank == card.rank]
        for c in cards_to_give:
            opponent_hand.remove(c)
            player_hand.append(c)
        dialog_messages.append(f"Компьютер отдает карты: {card.rank}")
        print(f"Компьютер отдает карты: {cards_to_give}")
        player_turn_continues = True  # Игрок продолжает ход
        check_full_set(player_hand, dialog_messages, is_player=True)  # Добавлено здесь
    else:
        # У компьютера нет карты
        dialog_messages.append("Нет человек, берите карту")
        player_turn_continues = False  # Ход переходит к компьютеру

# Ход компьютера        
def computer_turn(player_hand, computer_hand, dialog_messages, deck):
    global current_turn, requested_card, player_turn_continues
    print(">>> computer_turn called, current_turn:", current_turn)
    
    # Отладка: Начало хода компьютера
    print("Начало хода компьютера")
    
    if not player_turn_continues:
        if computer_hand:
            random_card = random.choice(computer_hand)
            dialog_messages.append(f"У вас есть {random_card.rank}, человек?")
            print(f"Компьютер спрашивает у игрока карту: {random_card.rank}")
            requested_card = random_card.rank
            current_turn = 'Ожидание ответа игрока'
            # Отладка: Запрашиваемая карта и текущий ход
            print(f"Компьютер запросил карту: {random_card.rank}, текущий ход: {current_turn}")

        else:
            dialog_messages.append("У компьютера нет карт, ход переходит к человеку")
            print("У компьютера нет карт, ход переходит к игроку")
            current_turn = 'Игрок'
            requested_card = None
            # Отладка: Ответ игрока на запрос компьютера
            print(f"Обработка ответа игрока, запрошенная карта: {requested_card}, текущий ход: {current_turn}")
    else:
        if requested_card in [c.rank for c in player_hand]:
            # У игрока есть карта, отдать все карты этого номинала
            cards_to_give = [c for c in player_hand if c.rank == requested_card]
            for c in cards_to_give:
                player_hand.remove(c)
                computer_hand.append(c)
            dialog_messages.append(f"Игрок отдает карты: {requested_card}")
            print(f"Игрок отдает карты: {cards_to_give}")
            player_turn_continues = False  # Ход переходит к игроку
        else:
            # Компьютер берет карту, если у игрока нет запрашиваемой карты
            computer_draw_card(deck, computer_hand, dialog_messages)
            current_turn = 'Игрок'
        requested_card = None
        print("Конец хода компьютера")
        
def computer_draw_card(deck, computer_hand, dialog_messages):
    """Компьютер берет карту из колоды."""
    new_card = deck.draw_card()
    if new_card:
        computer_hand.append(new_card)
        dialog_messages.append("Компьютер взял карту")
        print(f"Компьютер взял карту: {new_card}")
        check_full_set(computer_hand, dialog_messages, is_player=False)  # Добавлено здесь
    else:
        dialog_messages.append("В колоде больше нет карт")
        
# Игровые объекты
deck = Deck()
players = [Player("Игрок"), Player("Компьютер", is_human=False)]
deal_cards(deck, players)

def add_cards_to_hand(hand, cards_to_add, dialog_messages):
    """Добавление карт к руке игрока с учетом номинала."""
    for card in cards_to_add:
        hand.append(card)  # Добавляем карты в конец руки
    print(f"Карты добавлены в руку: {hand}")
    check_full_set(hand, dialog_messages, is_player=(hand == players[0].hand))

# Функция для проверки и обработки сбора полного набора карт
def check_full_set(hand, dialog_messages, is_player):
    global player_chests_collected, computer_chests_collected

    for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
        if len([card for card in hand if card.rank == rank]) == 4:
            # Удаление всех карт этого номинала из руки
            hand[:] = [card for card in hand if card.rank != rank]
            dialog_messages.append("Вот и собран еще один набор карт")
            if is_player:
                player_chests_collected += 1
            else:
                computer_chests_collected += 1
                
# Функция для отрисовки счетчиков сундучков
def draw_chest_counters():
    player_counter_text = button_font.render(f"{player_chests_collected}", True, (0, 255, 0))
    computer_counter_text = button_font.render(f"{computer_chests_collected}", True, (0, 255, 0))

    # Отрисовка счетчика игрока (снизу)
    screen.blit(player_counter_text, (SCREEN_WIDTH - CHEST_SIZE - 60, SCREEN_HEIGHT - CHEST_SIZE - 10))

    # Отрисовка счетчика компьютера (сверху)
    screen.blit(computer_counter_text, (SCREEN_WIDTH - CHEST_SIZE - 60, 20))
            
# Функция для взятия карты игроком из колоды
def player_draw_card(deck, player_hand, dialog_messages):
    """Игрок берет карту из колоды."""
    new_card = deck.draw_card()
    if new_card:
        player_hand.append(new_card)
        dialog_messages.append("Игрок взял карту")
        print(f"Игрок взял карту: {new_card}")
    else:
        dialog_messages.append("В колоде больше нет карт")

# Функция для расположения карт игрока по центру снизу экрана
def draw_hand(hand, y_pos, is_player):
    if is_player:
        # Отрисовка карт игрока в стопку
        grouped_hand = group_cards_by_rank(hand)
        start_x = (SCREEN_WIDTH - (len(grouped_hand) * (CARD_WIDTH + 30) - 30)) // 2
        for group in grouped_hand.values():
            for i, card in enumerate(group):
                screen.blit(card.image, (start_x, y_pos - i * 30))
            start_x += CARD_WIDTH + 10
    else:
        # Отрисовка карт компьютера в ряд
        start_x = (SCREEN_WIDTH - (len(hand) * (CARD_WIDTH + 10) - 10)) // 2
        for i, card in enumerate(hand):
            screen.blit(back_card_image, (start_x + i * (CARD_WIDTH + 10), y_pos))

# Отображение колоды карт и создание прямоугольника для обработки событий клика
def draw_deck(deck, x_pos, y_pos):
    global deck_rect  # Определяем deck_rect как глобальную переменную
    if deck.cards:
        screen.blit(back_card_image, (x_pos, y_pos))
        deck_rect = pygame.Rect(x_pos, y_pos, CARD_WIDTH, CARD_HEIGHT)  # Создаем прямоугольник для колоды
    else:
        deck_rect = None  # Если в колоде нет карт, deck_rect не определен
        
# Определение, кто начинает игру
current_turn = random.choice(['Игрок', 'Компьютер'])
dialog_messages = ["Игра началась"]
if current_turn == 'Игрок':
    dialog_messages.append("Ваш ход, человек")
else:
    dialog_messages.append("Ваш ход, компьютер")
    computer_turn(players[0].hand, players[1].hand, dialog_messages, deck)
    print("После хода компьютера, текущий ход: ", current_turn)

# Основной игровой цикл
menu_background = load_background_image('menu.jpg')
rules_background = load_background_image('rules.jpg')
about_background = load_background_image('about.jpg')
settings_background = load_background_image('settings.jpg')
load_background_music()  # Загрузка и воспроизведение музыки
buttons = create_buttons(SCREEN_WIDTH, SCREEN_HEIGHT)
return_button = pygame.Rect(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 60, 200, 50)  # Кнопка "Вернуться"

slider_value = 0.5  # Начальное значение громкости (от 0 до 1)
# Создание прямоугольника для слайдера
slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 20)  # Обновлено для соответствия функции draw_settings_screen
handle_rect = pygame.Rect(0, 0, 20, 30)  # Обновлено для соответствия функции draw_settings_screen
# Добавляем переменную для отслеживания зажатия кнопки мыши
is_sliding = False

# Анимация текста "О разработчике"
text_y_pos = SCREEN_HEIGHT // 2
animation_speed = 0.05  # Скорость анимации (меньше значение - быстрее анимация)
last_update_time = time.time()

menu_button = pygame.Rect(10, 10, 100, 40)  # Позиция и размер кнопки
# Установка начального состояния
current_state = "menu"
running = True

while running:
    current_time = time.time()
    time_delta = current_time - last_update_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                response = handle_menu_click(mouse_pos, buttons)
                if response == "Старт игры":
                    pygame.mixer.music.stop()
                    load_game_music()
                    current_state = "game"
                elif response == "Правила":
                    current_state = "rules"
                elif response == "О разработчике":
                    current_state = "about"
                elif response == "Настройки":
                    current_state = "settings"
                elif response == "Выход из игры":
                    running = False

        elif current_state == "rules":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    current_state = "menu"

        elif current_state == "about":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    current_state = "menu"

            # Обновление анимации текста
            if time_delta > animation_speed:
                text_y_pos -= 1
                if text_y_pos < 0:
                    text_y_pos = SCREEN_HEIGHT
                last_update_time = current_time

        elif current_state == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    current_state = "menu"
                elif slider_rect.collidepoint(event.pos):
                    is_sliding = True  # Начинаем слайдинг
                    x, _ = event.pos
                    slider_value = (x - slider_rect.left) / slider_rect.width
                    pygame.mixer.music.set_volume(slider_value)
                    handle_rect.centerx = slider_rect.left + int(slider_rect.width * slider_value)
            elif event.type == pygame.MOUSEBUTTONUP:
                is_sliding = False  # Заканчиваем слайдинг
            elif event.type == pygame.MOUSEMOTION and is_sliding:
                x, _ = event.pos
                slider_value = max(0, min(1, (x - slider_rect.left) / slider_rect.width))
                handle_rect.centerx = slider_rect.left + int(slider_rect.width * slider_value)
                pygame.mixer.music.set_volume(slider_value)

        elif current_state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()  # Останавливаем музыку игры
                    load_background_music()  # Запускаем музыку меню
                    current_state = "menu"
                button_rect = draw_button()
                # Проверка нажатия на кнопку "Нет такой карты"
                if button_rect.collidepoint(event.pos) and current_turn == 'Ожидание ответа игрока':
                    dialog_messages.append("Нет, компьютер, тяните карту")
                    computer_draw_card(deck, players[1].hand, dialog_messages)
                    current_turn = 'Игрок'
                    requested_card = None
                    continue

                # Проверка нажатия на колоду карт для взятия карты игроком
                if deck_rect and deck_rect.collidepoint(event.pos) and current_turn == 'Игрок':
                    player_draw_card(deck, players[0].hand, dialog_messages)
                    if not player_turn_continues:
                        current_turn = 'Компьютер'
                    continue

                # Логика хода игрока
                if current_turn == 'Игрок':
                    clicked_card = card_clicked(players[0].hand, *event.pos)
                    if clicked_card:  # Проверяем, что clicked_card не None
                        player_turn(clicked_card, players[0].hand, players[1].hand, dialog_messages)

                # Логика ответа игрока на ход компьютера
                if current_turn == 'Ожидание ответа игрока':
                    clicked_card = card_clicked(players[0].hand, *event.pos)
                    if clicked_card and clicked_card.rank == requested_card:
                        # Игрок отдает все карты этого ранга компьютеру
                        cards_to_give = [card for card in players[0].hand if card.rank == requested_card]
                        for card in cards_to_give:
                            players[0].hand.remove(card)
                            players[1].hand.append(card)
                        dialog_messages.append(f"Игрок отдает карты: {requested_card}")
                        current_turn = 'Компьютер'
                    elif clicked_card:
                        # Компьютер берет карту из колоды, если у игрока нет запрашиваемой карты
                        dialog_messages.append("У вас нет такой карты, компьютер берет карту")
                        computer_draw_card(deck, players[1].hand, dialog_messages)
                        current_turn = 'Игрок'
                    requested_card = None

            # Обработка хода компьютера
            if current_turn == 'Компьютер':
                computer_turn(players[0].hand, players[1].hand, dialog_messages, deck)

    # Рендеринг фона и интерфейсных элементов
    if current_state == "menu":
        draw_menu(screen, buttons, menu_background)
    elif current_state == "rules":
        screen.blit(rules_background, (0, 0))
        draw_rules_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, pygame.mouse.get_pos(), "rules_text.txt")
        draw_button_menu(screen, return_button, "Вернуться", check_hover(return_button, pygame.mouse.get_pos()))

    elif current_state == "about":
        screen.blit(about_background, (0, 0))
        draw_about_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, pygame.mouse.get_pos(), text_y_pos, "about_text.txt")

        if time_delta > animation_speed:
            text_y_pos -= 1
            if text_y_pos < 0:
                text_y_pos = SCREEN_HEIGHT
            last_update_time = current_time
        draw_button_menu(screen, return_button, "Вернуться", check_hover(return_button, pygame.mouse.get_pos()))

    elif current_state == "settings":
        screen.blit(settings_background, (0, 0))
        draw_settings_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, pygame.mouse.get_pos(), slider_value, settings_background)
        draw_button_menu(screen, return_button, "Вернуться", check_hover(return_button, pygame.mouse.get_pos()))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if slider_rect.collidepoint(event.pos):
                # Если пользователь нажал на трек ползунка
                handle_rect.centerx = event.pos[0]
                slider_value = (handle_rect.centerx - slider_rect.left) / slider_rect.width
                pygame.mixer.music.set_volume(slider_value)  # Устанавливаем громкость

    elif current_state == "game":
        screen.blit(background_image, (0, 0))
        draw_hand(players[0].hand, SCREEN_HEIGHT - CARD_HEIGHT - 10, True)
        draw_hand(players[1].hand, 10, False)
        draw_deck(deck, SCREEN_WIDTH - CARD_WIDTH - 20, SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2)
        draw_button()
        draw_dialog_box(dialog_messages)
        draw_chests()
        draw_chest_counters()
        draw_button_menu(screen, menu_button, "Меню", check_hover(menu_button, pygame.mouse.get_pos()))

    pygame.display.flip()

pygame.quit()