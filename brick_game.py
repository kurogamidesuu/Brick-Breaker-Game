import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick game - Hime")

# Ball
ball_size = 10
ball_color = (255, 255, 255)
ball = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ball_size, ball_size)
ball_speed_x = 5
ball_speed_y = 5

# Tile
tile_height = 30
tile_width = 70
tile_color = (100, 150, 225)
def reset_tiles():
    return [[pygame.Rect(5 + i * (tile_width + 10), 5 + j * (tile_height + 10), tile_width, tile_height) for i in range(10)] for j in range(5)]

tiles = reset_tiles()

# Platform
platform_height = 10
platform_width = 100
platform_color = (255, 255, 255)
platform = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT - platform_height, platform_width, platform_height)

font = pygame.font.Font(None, 74)
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
overlay.fill((255, 255, 255, 128))

paused = False
game_over = False

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game_over:
                paused = not paused
            if game_over and event.key == pygame.K_r:
                game_over = False
                paused = False
                ball.x = SCREEN_WIDTH / 2
                ball.y = SCREEN_HEIGHT / 2
                ball_speed_x = 5
                ball_speed_y = 5
                tiles = reset_tiles()

    # ball
    pygame.draw.ellipse(screen, ball_color, ball)

    if not paused:
        ball.move_ip(ball_speed_x, ball_speed_y)

        if ball.left < 0 or ball.right > SCREEN_WIDTH:
            ball_speed_x *= -1
        if ball.top < 0:
            ball_speed_y *= -1
        if ball.bottom > SCREEN_HEIGHT:
            ball.x = SCREEN_WIDTH / 2
            ball.y = SCREEN_HEIGHT / 2
            ball_speed_y  = -5
            game_over = True
            paused = True

    # platform
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        platform.move_ip(-10, 0)
    if key[pygame.K_d]:
        platform.move_ip(10, 0)

    pygame.draw.rect(screen, platform_color, platform)

    # tiles
    for row in tiles:
        for tile in row:
            pygame.draw.rect(screen, tile_color, tile)

    for row in tiles:
        for tile in row[:]:
            if ball.colliderect(tile):
                row.remove(tile)
                ball_speed_y *= -1
    if ball.colliderect(platform):
        ball_speed_y *= -1

    if paused:
        screen.blit(overlay, (0, 0))
        if not game_over:
            pause_text = font.render("PAUSED", True, (255, 255, 255))
        else:
            pause_text = font.render("GAME OVER!", True, (255, 255, 255))
            restart_text = font.render("Press 'R' to Restart", True, (255, 255, 255))
            screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(pause_text, (SCREEN_WIDTH / 2 - pause_text.get_width() / 2, SCREEN_HEIGHT / 2 - pause_text.get_height() / 2))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()