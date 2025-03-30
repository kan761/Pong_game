import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED_X_INITIAL = 6
BALL_SPEED_Y_INITIAL = 6

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- Game Functions ---
def ball_reset(ball, ball_speed_x, ball_speed_y):
    """Resets the ball to the center and gives it a random direction."""
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    # Randomize horizontal and vertical direction after reset
    ball_speed_x = BALL_SPEED_X_INITIAL * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y_INITIAL * random.choice((1, -1))
    return ball_speed_x, ball_speed_y

def move_paddle(keys, paddle, up_key, down_key):
    """Moves the paddle based on key presses, keeping it within bounds."""
    if keys[up_key] and paddle.top > 0:
        paddle.y -= PADDLE_SPEED
    if keys[down_key] and paddle.bottom < SCREEN_HEIGHT:
        paddle.y += PADDLE_SPEED

def draw_elements(screen, paddle_a, paddle_b, ball, score_a, score_b, font):
    """Draws all game elements onto the screen."""
    # Background
    screen.fill(BLACK)
    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)
    pygame.draw.ellipse(screen, WHITE, ball)
    # Draw center line
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Draw scores
    score_text_a = font.render(f"{score_a}", True, WHITE)
    screen.blit(score_text_a, (SCREEN_WIDTH // 4, 20))
    score_text_b = font.render(f"{score_b}", True, WHITE)
    screen.blit(score_text_b, (SCREEN_WIDTH * 3 // 4 - score_text_b.get_width(), 20))

# --- Main Game Setup ---
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Pong')

# Clock to control frame rate
clock = pygame.time.Clock()

# Game objects (using Rect for easy collision detection and drawing)
paddle_a = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Ball speed variables
ball_speed_x, ball_speed_y = BALL_SPEED_X_INITIAL, BALL_SPEED_Y_INITIAL
ball_speed_x, ball_speed_y = ball_reset(ball, ball_speed_x, ball_speed_y) # Initial random direction

# Score variables
score_a = 0
score_b = 0
game_font = pygame.font.Font(None, 74) # Default font, size 74

# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Key Presses for Paddle Movement ---
    keys = pygame.key.get_pressed()
    move_paddle(keys, paddle_a, pygame.K_w, pygame.K_s) # Player A: W (up), S (down)
    move_paddle(keys, paddle_b, pygame.K_UP, pygame.K_DOWN) # Player B: Up Arrow (up), Down Arrow (down)

    # --- Game Logic ---
    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1 # Reverse vertical direction

    # Ball collision with paddles
    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_speed_x *= -1 # Reverse horizontal direction
        # Optional: Add slight speed increase on paddle hit
        # ball_speed_x *= 1.05
        # ball_speed_y *= 1.05
        # ball_speed_x = min(ball_speed_x, 15) if ball_speed_x > 0 else max(ball_speed_x, -15) # Cap speed
        # ball_speed_y = min(ball_speed_y, 15) if ball_speed_y > 0 else max(ball_speed_y, -15) # Cap speed


    # Ball goes out of bounds (scoring)
    if ball.left <= 0:
        score_b += 1
        ball_speed_x, ball_speed_y = ball_reset(ball, ball_speed_x, ball_speed_y)
    elif ball.right >= SCREEN_WIDTH:
        score_a += 1
        ball_speed_x, ball_speed_y = ball_reset(ball, ball_speed_x, ball_speed_y)

    # --- Drawing ---
    draw_elements(screen, paddle_a, paddle_b, ball, score_a, score_b, game_font)

    # --- Update Display ---
    pygame.display.flip() # Update the full screen

    # --- Frame Rate Control ---
    clock.tick(60) # Limit game to 60 frames per second

# --- Quit Pygame ---
pygame.quit()
sys.exit()