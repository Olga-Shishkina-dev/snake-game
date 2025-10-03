import random

class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):
        WIDTH, HEIGHT = 800, 680
        CELL_SIZE = 20
        while True:
            x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            pos = (x, y)
            if pos not in snake_body:  # Проверка
                return pos

    def draw(self, surface):
        import pygame
        pygame.draw.rect(surface, (255, 0, 0), (self.position[0], self.position[1], 20, 20))
