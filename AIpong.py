import pygame  
import sys  
import random
  
# Initialize Pygame  
pygame.init()  
  
# Constants  
WIDTH, HEIGHT = 1700, 1000  
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
BLUE = (0, 0, 255)  
GREEN = (0, 255, 0)  
YELLOW = (255, 255, 0) 
RED = (255, 123, 46) 
  
# Create the screen  
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Action RPG with Pong")  
  
# Font for displaying score  
font = pygame.font.SysFont(None, 36)  
  
# Player properties  
player_size = 50  
player_speed = 5  
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, player_size, player_size)  
  
# Block properties  
block = pygame.Rect(300, 300, player_size, player_size)  
  
# Merchant properties  
sizemerchant = pygame.Rect(600, 200, player_size, player_size) 
speedmerchant = pygame.Rect(680, 200, player_size, player_size) 
  
score = 0
money = 0

# Pong elements  
paddle_width, paddle_height = 10, 100  
paddle_speed = 10  
cpu_paddle_speed = 7 + (score // 2)  # Slower CPU paddle speed  
ball_size = 100  
initial_ball_speed_x, initial_ball_speed_y = 3, 3  
ball_speed_x, ball_speed_y = initial_ball_speed_x, initial_ball_speed_y  
left_paddle = pygame.Rect(10, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)  
right_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)  
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)  
  
# Game states  
in_pong = False  
paddle_upgrade = 0    
  
# Set up the clock for frame limiting  
clock = pygame.time.Clock()  
FPS = 60  # Frames per second  
  
def get_non_zero_randint(low, high):  
    number = 0  
    while number == 0:  
        number = random.randint(low, high)  
    return number 

def move_cpu_paddle():  
    if ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:  
        right_paddle.y += cpu_paddle_speed  
    elif ball.centery < right_paddle.centery and right_paddle.top > 0:  
        right_paddle.y -= cpu_paddle_speed  
  
def reset_ball():  
    global ball_speed_x, ball_speed_y
    initial_ball_speed_x, initial_ball_speed_y = get_non_zero_randint(-3, 3), get_non_zero_randint(-3, 3)
    ball_speed_x, ball_speed_y = initial_ball_speed_x, initial_ball_speed_y  
    ball.x, ball.y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2  
    ball_speed_x, ball_speed_y = initial_ball_speed_x, initial_ball_speed_y   
  
def upgrade_paddle(paddle_upgrade):  
    global left_paddle  
    left_paddle.height = paddle_height + (paddle_upgrade * 2)
  
def display_score():  
    score_text = font.render(f'Score: {score}', True, WHITE)  
    money_text = font.render(f'Money: {money}', True, WHITE)
    screen.blit(score_text, (10, 10))  
    screen.blit(money_text, (150, 10)) 
  
# Main game loop  
running = True  
while running:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
    cpu_paddle_speed = 7 + (score // 2)
  
    keys = pygame.key.get_pressed()  
  
    if in_pong:  
        if paddle_upgrade:  
            upgrade_paddle(paddle_upgrade)  
        if keys[pygame.K_w] and left_paddle.top > 0:  
            left_paddle.y -= paddle_speed  
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:  
            left_paddle.y += paddle_speed  
  
        move_cpu_paddle()  
  
        ball.x += ball_speed_x * 3  
        ball.y += ball_speed_y * 3
  
        if ball.top <= 0 or ball.bottom >= HEIGHT:  
            ball_speed_y *= -1.1 
  
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):  
            ball_speed_x *= -1.5
  
        if ball.right > WIDTH + 100:  
            in_pong = False  
            score += 1  # Increase score when exiting Pong  
            money += 10
            reset_ball()  
            left_paddle.height = paddle_height  
  
        if ball.left < 0 - 100 :  
            reset_ball()  
            ball_speed_x *= -1  
  
        screen.fill(BLACK)  
        pygame.draw.rect(screen, WHITE, left_paddle)  
        pygame.draw.rect(screen, WHITE, right_paddle)  
        pygame.draw.ellipse(screen, WHITE, ball)  
  
    else:  
        if keys[pygame.K_LEFT]:  
            player.x -= player_speed  
        if keys[pygame.K_RIGHT]:  
            player.x += player_speed  
        if keys[pygame.K_UP]:  
            player.y -= player_speed  
        if keys[pygame.K_DOWN]:  
            player.y += player_speed  
  
        if player.colliderect(block) and keys[pygame.K_SPACE]:  
            in_pong = True  
            reset_ball()  
  
        if player.colliderect(sizemerchant) and keys[pygame.K_SPACE]:  
            if money > 0:
                paddle_upgrade += 1.5
                money -= 1

        if player.colliderect(speedmerchant) and keys[pygame.K_SPACE]:  
            if money > 0:
                paddle_speed += 0.5
                money -= 1
  
        screen.fill(BLACK)  
        pygame.draw.rect(screen, GREEN, player)  
        pygame.draw.rect(screen, BLUE, block)  
        pygame.draw.rect(screen, YELLOW, sizemerchant) 
        pygame.draw.rect(screen, RED, speedmerchant) 
  
        display_score()  
  
    pygame.display.flip()  
      
    clock.tick(FPS)  
  
pygame.quit()  
sys.exit()  
