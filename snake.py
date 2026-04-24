import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
window_width = 600
window_height = 600
cell_size = 20
cell_number_x = window_width // cell_size
cell_number_y = window_height // cell_size

# Цвета (RGB)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
dark_green = (0, 200, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Настройки окна
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.body = [(cell_number_x // 2, cell_number_y // 2)]
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
        if (head[0] < 0 or head[0] >= cell_number_x or
            head[1] < 0 or head[1] >= cell_number_y):
            return True
        # Столкновение с собой
        if head in self.body[1:]:
            return True
        return False
    
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, green, 
                           (segment[0] * cell_size, segment[1] * cell_size, 
                            cell_size, cell_size))
            pygame.draw.rect(screen, dark_green, 
                           (segment[0] * cell_size, segment[1] * cell_size, 
                            cell_size, cell_size), 2)

class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)
    
    def random_position(self, snake_body):
        while True:
            pos = (random.randint(0, cell_number_x - 1),
                  random.randint(0, cell_number_y - 1))
            if pos not in snake_body:
                return pos
    
    def draw(self):
        pygame.draw.rect(screen, red, 
                        (self.position[0] * cell_size, self.position[1] * cell_size,
                         cell_size, cell_size))

def show_game_over(score):
    screen.fill(black)
    game_over_text = font.render("Вы проиграли!", True, red)
    score_text = font.render(f"Очки: {score}", True, white)
    restart_text = font.render("Нажмите пробел, чтобы начать заново", True, white)
    
    screen.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, 
                                 window_height // 2 - 60))
    screen.blit(score_text, (window_width // 2 - score_text.get_width() // 2, 
                            window_height // 2 - 20))
    screen.blit(restart_text, (window_width // 2 - restart_text.get_width() // 2, 
                              window_height // 2 + 20))
    
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
        screen.fill(black)
        snake.draw()
        food.draw()
        
        # Отображение счета
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(10)  # Скорость игры
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
