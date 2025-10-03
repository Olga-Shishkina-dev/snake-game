import pygame
import sys
import random
import os
from snake import Snake
from food import Food

pygame.init()
pygame.mixer.init()

# Путь к папке с ассетами
ASSETS_DIR = "assets"

# --- Загрузка звуков с обработкой ошибок ---
def load_sound(filename):
    path = os.path.join(ASSETS_DIR, filename)
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        print(f"Звуковой файл '{filename}' не найден или не может быть загружен.")
        return None

def load_music(filename):
    path = os.path.join(ASSETS_DIR, filename)
    try:
        pygame.mixer.music.load(path)
        return True
    except pygame.error:
        print(f"Музыкальный файл '{filename}' не найден или не может быть загружен.")
        return False

# Загружаем музыку и звук еды
music_loaded = load_music("фон.wav")
eat_sound = load_sound("хрум.wav")

# --- Константы ---
SIZE = (800, 680)
CELL_SIZE = 20
WIDTH, HEIGHT = SIZE
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (30, 92, 169)
COLOR_INACTIVE = pygame.Color(173, 216, 230)
COLOR_ACTIVE = pygame.Color(250, 250, 0)

# --- Фон ---
try:
    background_image = pygame.image.load(os.path.join(ASSETS_DIR, "песок.jpg"))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error:
    background_image = None
    print("Фоновое изображение не найдено.")

# --- Рекорд ---
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        # Создаём файл с 0, если нет
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write("0")
        except OSError:
            print("Ошибка создания файла рекорда.")
            return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip())
    except (ValueError, OSError):
        print("Ошибка чтения файла рекорда.")
        return 0

def save_highscore(highscore):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(highscore))
    except OSError:
        print("Ошибка сохранения рекорда.")

# --- Упрощённое меню выбора сложности ---
difficulty_options = ["легко", "нормально", "трудно", "невозможно"]
selected_index = 0
hover_index = -1

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def check_mouse_over(mouse_pos):
    global hover_index, selected_index
    start_y = HEIGHT // 2
    step_y = 60
    x_mouse, y_mouse = mouse_pos
    hover_index = -1
    for i, option in enumerate(difficulty_options):
        text_surface = font.render(option, True, COLOR_ACTIVE if i == selected_index else COLOR_INACTIVE)
        text_x = WIDTH // 2 - text_surface.get_width() // 2
        text_y = start_y + i * step_y
        rect = pygame.Rect(text_x, text_y, text_surface.get_width(), text_surface.get_height())
        if rect.collidepoint(x_mouse, y_mouse):
            hover_index = i
            selected_index = i
            break

def show_difficulty_menu():
    global selected_index, hover_index
    start_y = HEIGHT // 2
    step_y = 60

    while True:
        screen.fill(BLACK)
        title_text = font.render("Выберите сложность", True, WHITE)
        title_x = WIDTH // 2 - title_text.get_width() // 2
        title_y = HEIGHT // 6
        screen.blit(title_text, (title_x, title_y))

        # Отображаем опции в цикле
        for i, option in enumerate(difficulty_options):
            color = COLOR_ACTIVE if i == selected_index or i == hover_index else COLOR_INACTIVE
            option_text = font.render(option, True, color)
            x = WIDTH // 2 - option_text.get_width() // 2
            y = start_y + i * step_y
            screen.blit(option_text, (x, y))

        pygame.display.flip()
        clock.tick(38)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(difficulty_options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    return difficulty_options[selected_index]
            elif event.type == pygame.MOUSEMOTION:
                check_mouse_over(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_mouse_over(event.pos)
                return difficulty_options[selected_index]

# Установка скорости в зависимости от выбранного уровня сложности
def set_speed(difficulty):
    if difficulty == "легко":
        print("Выбран уровень сложности: легко")
        return 5
    elif difficulty == "нормально":
        print("Выбран уровень сложности: нормально")
        return 10
    elif difficulty == "трудно":
        print("Выбран уровень сложности: трудно")
        return 15
    elif difficulty == "невозможно":
        print("Выбран уровень сложности: невозможно")
        return 20

# Экран инструкции для игры
def show_instructions():
    screen.fill(BLACK)
    title_text = font.render("Инструкция", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    instructions = [
        "Управление: Стрелки для движения",
        "Цель: Собирать еду (красные квадраты), избегать стен и себя",
        "P - Пауза, ESC - Выход",
        "Нажмите ENTER для старта"
    ]
    for i, line in enumerate(instructions):
        line_text = small_font.render(line, True, WHITE)
        screen.blit(line_text, (WIDTH // 2 - line_text.get_width() // 2, 150 + i * 50))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Экран окончания игры
def show_game_over(score, highscore):
    screen.fill(BLACK)
    game_over_text = font.render("Игра окончена!", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

    score_text = small_font.render(f"Ваш счёт: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 100))

    highscore_text = small_font.render(f"Рекорд: {highscore}", True, WHITE)
    screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 3 + 150))

    restart_text = small_font.render("Нажмите R для перезапуска или ESC для выхода", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 3 + 200))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Перезапуск
                elif event.key == pygame.K_ESCAPE:
                    return False  # Выход

def handle_keys(event, snake, paused):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p:
            return not paused  # Переключение паузы
        elif not paused:  # Игнорировать управление во время паузы
            if event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.change_direction((1, 0))
    return paused

def main():
    highscore = load_highscore()
    difficulty = show_difficulty_menu()  # Получаем выбранную сложность
    show_instructions()
    if music_loaded:
        pygame.mixer.music.play(-1)
    speed = set_speed(difficulty)  # Устанавливаем скорость

    snake = Snake()
    food = Food(snake.body)  # Создаём еду, передавая тело змеи
    score = 0
    paused = False

    running = True
    while running:
        clock.tick(speed)  # Регулируем скорость игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Мягкий стоп цикла
            paused = handle_keys(event, snake, paused)

        if not paused:
            snake.move()

        # Проверка поедания еды
        if snake.body[0] == food.position:
            score += 1
            snake.grow = True  # Змея растёт
            food = Food(snake.body)  # Перегенерируем еду
            if eat_sound:
                eat_sound.play()  # Воспроизведение звука при съедании еды
            speed = min(speed + 1, 50)  # Постепенное ускорение

        # Проверка на выход за границы
        if (snake.body[0][0] < 0 or snake.body[0][0] >= SIZE[0] or
            snake.body[0][1] < 0 or snake.body[0][1] >= SIZE[1]):
            running = False

        # Проверка на столкновение с телом
        if snake.body[0] in snake.body[1:]:
            running = False

        screen.fill(BLACK)
        if background_image:
            screen.blit(background_image, (0, 0))  # Блитируем фон
        snake.draw(screen)
        food.draw(screen)

        # Отображение счёта
        score_text = small_font.render(f"Счёт: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        highscore_text = small_font.render(f"Рекорд: {highscore}", True, WHITE)
        screen.blit(highscore_text, (10, 50))

        if paused:
            pause_text = font.render("Пауза", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    # Обновляем рекорд (только если новый рекорд лучше)
    if score > highscore:
        highscore = score
        save_highscore(highscore)

    # Экран окончания
    if show_game_over(score, highscore):
        main()  # Перезапуск
    else:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
