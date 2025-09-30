import pygame
import sys
import random
import webbrowser

pygame.init()


WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)


WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

def draw_snake(snake):
    for pos in snake:
        rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

def draw_food(food):
    rect = pygame.Rect(food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)

def check_collision(snake):
    head = snake[0]
    
    if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
        return True
    
    if head in snake[1:]:
        return True
    return False

def place_food(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def restart_game():
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (0, -1)
    food = place_food(snake)
    score = 0
    return snake, direction, food, score

snake, direction, food, score = restart_game()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
            else:
                if event.key == pygame.K_r:
                    snake, direction, food, score = restart_game()
                    game_over = False

    if not game_over:
        
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        
        if new_head == food:
            score += 1
            food = place_food(snake)
        else:
            snake.pop()

        
        if check_collision(snake):
            game_over = True

        
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))
        #Edit it to prevent the link  from openoing
        if(score==3):
            webbrowser.open('https://www.youtube.com/watch?v=v3m3mphkLk0')
            score+=1 
    else:
        # Game over screen
        screen.fill(BLACK)
        over_surface = font.render("Game Over!", True, RED)
        restart_surface = font.render("Press R to Restart", True, WHITE)
        score_surface = font.render(f"Score: {score}", True, GREEN)
        screen.blit(over_surface, (WIDTH // 2 - over_surface.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.update()
    clock.tick(10)