import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker Game - by Kuro")

# Ball
ball_size = 10
ball_color = (255, 7, 58)
ball = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ball_size, ball_size)
ball_speed_x = 5
ball_speed_y = 5

# Tile
tile_height = 30
tile_width = 70
tile_color = (100, 150, 225)

def reset_tiles():
    return [[pygame.Rect(5 + i * (tile_width + 10), 100 + j * (tile_height + 10), tile_width, tile_height) for i in range(10)] for j in range(5)]

tiles = reset_tiles()

brick_colors = [
    (255, 69, 0),
    (255, 215, 0),
    (50, 205, 50),
    (30, 144, 255),
    (148, 0, 211)
]

# Platform
platform_height = 10
platform_width = 100
platform_color = (0, 255, 255)
platform = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT - platform_height, platform_width, platform_height)

font = pygame.font.Font(None, 74)
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 200))

border = pygame.Rect(0, 75, SCREEN_WIDTH, 5)

score = 0
tiles_left = 50

paused = False
game_over = False
victory = False

pygame.mixer.music.load('C:/Coding/Python/Projects/Brick-Breaker-Game/assets/background_music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

gameover_sound = pygame.mixer.Sound("Projects/Brick-Breaker-Game/assets/gameover.wav")
victory_sound = pygame.mixer.Sound("Projects/Brick-Breaker-Game/assets/victory.wav")
gameover_sound.set_volume(0.5)
victory_sound.set_volume(0.5)

gameover_music_played = False
victory_sound_played = False

def reset_game():
    global score, tiles_left, game_over, paused, victory, tiles, gameover_music_played, victory_sound_played
    score = 0
    tiles_left = 50
    game_over = False
    paused = False
    victory = False
    tiles = reset_tiles()
    pygame.mixer.music.play(-1)
    gameover_music_played = False
    victory_sound_played = False

def create_gradient_surface(width, height, start_color, end_color):
    surface = pygame.Surface((width, height))
    for y in range(height):
        t = y / height
        r = start_color[0] + (end_color[0] - start_color[0]) * t
        g = start_color[1] + (end_color[1] - start_color[1]) * t
        b = start_color[2] + (end_color[2] - start_color[2]) * t
        pygame.draw.line(surface, (int(r), int(g), int(b)), (0, y), (width, y))
    return surface

gradient_surface = create_gradient_surface(SCREEN_WIDTH, SCREEN_HEIGHT, (13, 13, 30), (50, 0, 100))

running = True
while running:
    screen.blit(gradient_surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game_over:
                paused = not paused
            if (game_over or victory) and event.key == pygame.K_r:
                reset_game()
                ball.x = SCREEN_WIDTH / 2
                ball.y = SCREEN_HEIGHT / 2
                ball_speed_x = random.uniform(-5, 5)
                ball_speed_y = 5
                platform.left = SCREEN_WIDTH / 2 - platform_width / 2

    if tiles_left == 0:
        victory = True
        paused = True

    score_text = font.render(f"Score : {score}", True, (220, 210, 10))
    screen.blit(score_text, (10, 10))
    pygame.draw.rect(screen, (155, 77, 155), border)

    # ball
    pygame.draw.ellipse(screen, ball_color, ball)

    if not paused:
        pygame.mixer.music.unpause()
        ball.move_ip(ball_speed_x, ball_speed_y)

        if ball.left < 0 or ball.right > SCREEN_WIDTH:
            ball_speed_x *= -1
        if ball.colliderect(border):
            ball_speed_y *= -1
        if ball.bottom > SCREEN_HEIGHT:
            ball.x = SCREEN_WIDTH / 2
            ball.y = SCREEN_HEIGHT / 2
            ball_speed_y  = -5
            game_over = True
            paused = True

        # platform
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and platform.left > 0:
            platform.move_ip(-10, 0)
        if key[pygame.K_d] and platform.right < SCREEN_WIDTH:
            platform.move_ip(10, 0)

    pygame.draw.rect(screen, platform_color, platform)

    # tiles
    for i, row in enumerate(tiles):
        for tile in row:
            pygame.draw.rect(screen, brick_colors[i], tile)


    for row in tiles:
        for tile in row[:]:
            if ball.colliderect(tile):
                row.remove(tile)
                ball_speed_y *= -1
                score += 10
                tiles_left -= 1

    if ball.colliderect(platform):
        hit_position = (ball.centerx - platform.left) / platform_width
        ball_speed_x = (hit_position - 0.5) * 10
        ball_speed_y *= -1

    pause_text = font.render("PAUSED", True, (192, 192, 192))
    restart_text = font.render("Press 'R' to Restart", True, (0, 255, 128))
    victory_text = font.render("YOU WON!", True, (255, 215, 0))
    game_over_text = font.render("GAME OVER!", True, (255, 7, 58))

    if paused:
        pygame.mixer.music.pause()
        screen.blit(overlay, (0, 0))
        if game_over:
            if not gameover_music_played:
                gameover_sound.play()
                gameover_music_played = True
            screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2))
            screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() / 2, SCREEN_HEIGHT / 2 + 50))
        elif victory:
            if not victory_sound_played:
                victory_sound.play()
                victory_sound_played = True
            screen.blit(victory_text, (SCREEN_WIDTH / 2 - victory_text.get_width() / 2, SCREEN_HEIGHT / 2))
            screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() / 2, SCREEN_HEIGHT / 2 + 50))
        else:
            screen.blit(pause_text, (SCREEN_WIDTH / 2 - pause_text.get_width() / 2, SCREEN_HEIGHT / 2 - pause_text.get_height() / 2))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()