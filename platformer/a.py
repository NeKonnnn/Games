import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Platformer")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Загрузка изображений
player_img = pygame.image.load('player.png')
enemy_img = pygame.image.load('enemy.png')
coin_img = pygame.image.load('coin.png')
platform_img = pygame.image.load('platform.png')

# Изменение размера изображений
player_img = pygame.transform.scale(player_img, (50, 60))
enemy_img = pygame.transform.scale(enemy_img, (50, 60))
coin_img = pygame.transform.scale(coin_img, (20, 20))
platform_img = pygame.transform.scale(platform_img, (100, 20))

# Игрок
player_width, player_height = 50, 60
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10
player_vel = 5
player_jump = False
player_jump_count = 10
player_health = 100
player_alive = True

# Враги
enemy_width, enemy_height = 50, 60
enemies = [(random.randint(0, WIDTH - enemy_width), random.randint(0, HEIGHT - enemy_height)) for _ in range(5)]

# Платформы
platform_width, platform_height = 100, 20
platforms = [(random.randint(0, WIDTH - platform_width), random.randint(HEIGHT // 2, HEIGHT - platform_height)) for _ in range(5)]

# Монеты
coin_width, coin_height = 20, 20
coins = [(random.randint(0, WIDTH - coin_width), random.randint(0, HEIGHT - coin_height)) for _ in range(10)]
score = 0

# Оружие
weapon_types = ["pistol", "rifle"]
current_weapon = weapon_types[0]
weapon_damage = {"pistol": 10, "rifle": 20}

# Основной игровой цикл
run = True
while run:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if player_alive:
        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - player_vel > 0:
            player_x -= player_vel
        if keys[pygame.K_RIGHT] and player_x + player_vel < WIDTH - player_width:
            player_x += player_vel
        if not player_jump:
            if keys[pygame.K_SPACE]:
                player_jump = True
        else:
            if player_jump_count >= -10:
                neg = 1
                if player_jump_count < 0:
                    neg = -1
                player_y -= (player_jump_count ** 2) * 0.5 * neg
                player_jump_count -= 1
            else:
                player_jump = False
                player_jump_count = 10
        
        # Атака оружием
        if keys[pygame.K_a]:
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
                if player_rect.colliderect(enemy_rect):
                    enemies.remove(enemy)

        # Проверка столкновения с монетами
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for coin in coins[:]:
            coin_rect = pygame.Rect(coin[0], coin[1], coin_width, coin_height)
            if player_rect.colliderect(coin_rect):
                coins.remove(coin)
                score += 1

        # Проверка столкновения с врагами
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if player_rect.colliderect(enemy_rect):
                player_health -= 20
                if player_health <= 0:
                    player_alive = False

        # Отрисовка объектов
        win.fill(WHITE)
        win.blit(player_img, (player_x, player_y))
        for platform in platforms:
            win.blit(platform_img, (platform[0], platform[1]))
        for coin in coins:
            win.blit(coin_img, (coin[0], coin[1]))
        for enemy in enemies:
            win.blit(enemy_img, (enemy[0], enemy[1]))

        # Отображение счета и здоровья
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, BLACK)
        health_text = font.render(f'Health: {player_health}', True, BLACK)
        weapon_text = font.render(f'Weapon: {current_weapon}', True, BLACK)
        win.blit(score_text, (10, 10))
        win.blit(health_text, (10, 50))
        win.blit(weapon_text, (10, 90))

        pygame.display.update()

pygame.quit()