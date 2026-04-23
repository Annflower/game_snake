import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20
CELL_NUMBER_X = WINDOW_WIDTH // CELL_SIZE
CELL_NUMBER_Y = WINDOW_HEIGHT // CELL_SIZE

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Настройки окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.body = [(CELL_NUMBER_X // 2, CELL_NUMBER_Y // 2)]
        self.direction = (1, 0)  # вправо
        self.grow_flag = False
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        self.body.insert(0, new_head)
        
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
    
    def grow(self):
        self.grow_flag = True
    
    def check_collision(self):
        head = self.body[0]
        # Столкновение со стенами
        if (head[0] < 0 or head[0] >= CELL_NUMBER_X or
            head[1] < 0 or head[1] >= CELL_NUMBER_Y):
            return True
        # Столкновение с собой
        if head in self.body[1:]:
            return True
        return False
    
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, 
                           (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, 
                            CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, DARK_GREEN, 
                           (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, 
                            CELL_SIZE, CELL_SIZE), 2)

class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)
    
    def random_position(self, snake_body):
        while True:
            pos = (random.randint(0, CELL_NUMBER_X - 1),
                  random.randint(0, CELL_NUMBER_Y - 1))
            if pos not in snake_body:
                return pos
    
    def draw(self):
        pygame.draw.rect(screen, RED, 
                        (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))

def show_game_over(score):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to restart or ESC to quit", True, WHITE)
    
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                                 WINDOW_HEIGHT // 2 - 60))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 
                            WINDOW_HEIGHT // 2 - 20))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 
                              WINDOW_HEIGHT // 2 + 20))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    return False

def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0
    running = True
    
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
        
        # Движение
        snake.move()
        
        # Проверка столкновения
        if snake.check_collision():
            if not show_game_over(score):
                break
            else:
                # Перезапуск игры
                snake = Snake()
                food = Food(snake.body)
                score = 0
                continue
        
        # Проверка съедания еды
        if snake.body[0] == food.position:
            snake.grow()
            score += 1
            food = Food(snake.body)
        
        # Отрисовка
        screen.fill(BLACK)
        snake.draw()
        food.draw()
        
        # Отображение счета
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(10)  # Скорость игры
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

