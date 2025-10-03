import pygame

class Snake:
    def __init__(self):
        WIDTH, HEIGHT = 800, 680  # Используем константы из main, но для модульности дублируем
        CELL_SIZE = 20
        # Начинаем змею с 3 сегментов для лучшего вида
        self.body = [(WIDTH // 2, HEIGHT // 2),
                     (WIDTH // 2 - CELL_SIZE, HEIGHT // 2),
                     (WIDTH // 2 - CELL_SIZE * 2, HEIGHT // 2)]
        self.direction = (1, 0)  # Начинаем движение вправо
        self.grow = False

    def move(self):
        # Получаем текущую голову и создаем новую
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx * 20, head_y + dy * 20)  # Умножаем на CELL_SIZE

        self.body.insert(0, new_head)  # Добавляем новый сегмент в голову
        if self.grow:
            self.grow = False
        else:
            self.body.pop()  # Удаляем хвост

    def draw(self, surface):
        # Рисуем змею
        for part in self.body:
            pygame.draw.rect(surface, (0, 255, 0), (part[0], part[1], 20, 20))

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
