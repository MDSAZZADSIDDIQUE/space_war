import sys

import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("SPACE WAR")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60

VELOCITY = 5
BULLET_VELOCITY = 7

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 100

LEFT_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'left_spaceship.png'))
LEFT_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(LEFT_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

RIGHT_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'right_spaceship.png'))
RIGHT_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RIGHT_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_background.jpg')),
                                    (WIDTH, HEIGHT))

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bullets_firing.mp3'))
BULLET_FIRING_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bullets_hitting.mp3'))

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

LEFT_player_bullets = []
RIGHT_player_bullets = []

MAX_BULLETS = 3

LEFT_BULLET_HIT = pygame.USEREVENT + 1
RIGHT_BULLET_HIT = pygame.USEREVENT + 2

DISPLAY_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_TEXT_FONT = pygame.font.SysFont('comicsans', 100)


def draw_in_window(left_player, right_player, left_player_bullets, right_player_bullets, right_player_health,
                   left_player_health):
    WINDOW.blit(BACKGROUND, (0, 0))
    right_player_health_text = DISPLAY_FONT.render("Health: " + str(right_player_health), True, WHITE)
    left_player_health_text = DISPLAY_FONT.render("Health: " + str(left_player_health), True, WHITE)
    WINDOW.blit(right_player_health_text, (WIDTH - right_player_health_text.get_width(), 10))
    WINDOW.blit(left_player_health_text, (10, 10))
    WINDOW.blit(LEFT_SPACESHIP, (left_player.x, left_player.y))
    WINDOW.blit(RIGHT_SPACESHIP, (right_player.x, right_player.y))
    for bullet in left_player_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    for bullet in right_player_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    pygame.display.update()


def left_spaceship_movement(keys_pressed, left_player):
    if keys_pressed[pygame.K_a] and left_player.x - VELOCITY > 0:
        left_player.x -= VELOCITY
    if keys_pressed[pygame.K_d] and left_player.x + VELOCITY + left_player.width < BORDER.x:
        left_player.x += VELOCITY
    if keys_pressed[pygame.K_w] and left_player.y - VELOCITY > 0:
        left_player.y -= VELOCITY
    if keys_pressed[pygame.K_s] and left_player.y + VELOCITY + left_player.height < HEIGHT:
        left_player.y += VELOCITY


def right_spaceship_movement(keys_pressed, right_player):
    if keys_pressed[pygame.K_LEFT] and right_player.x - VELOCITY > BORDER.x + BORDER.width:
        right_player.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and right_player.x + VELOCITY + right_player.width < WIDTH:
        right_player.x += VELOCITY
    if keys_pressed[pygame.K_UP] and right_player.y - VELOCITY > 0:
        right_player.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and right_player.y + VELOCITY + right_player.height < HEIGHT:
        right_player.y += VELOCITY


def handle_bullets(left_player_bullets, right_player_bullets, left_player, right_player):
    for bullet in left_player_bullets:
        bullet.x += BULLET_VELOCITY
        if right_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LEFT_BULLET_HIT))
            left_player_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            left_player_bullets.remove(bullet)

    for bullet in right_player_bullets:
        bullet.x -= BULLET_VELOCITY
        if left_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIGHT_BULLET_HIT))
            right_player_bullets.remove(bullet)
        elif bullet.x < 0:
            right_player_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_TEXT_FONT.render(text, True, WHITE)
    WINDOW.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    right_player_health = 10
    left_player_health = 10
    left_player = pygame.Rect(200, 275, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    right_player = pygame.Rect(600, 275, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        winner_text = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(LEFT_player_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(left_player.x + left_player.width,
                                         left_player.y + left_player.height // 2, 10, 5)
                    LEFT_player_bullets.append(bullet)
                    BULLET_FIRING_SOUND.play()
                if event.key == pygame.K_RCTRL and len(RIGHT_player_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(right_player.x, right_player.y + right_player.height // 2, 10, 5)
                    RIGHT_player_bullets.append(bullet)
                    BULLET_FIRING_SOUND.play()
            if event.type == LEFT_BULLET_HIT:
                right_player_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RIGHT_BULLET_HIT:
                left_player_health -= 1
                BULLET_HIT_SOUND.play()
        if right_player_health <= 0:
            winner_text = "LEFT WINS"
        if left_player_health <= 0:
            winner_text = "RIGHT WINS"

        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        left_spaceship_movement(keys_pressed, left_player)
        right_spaceship_movement(keys_pressed, right_player)

        handle_bullets(LEFT_player_bullets, RIGHT_player_bullets, left_player, right_player)

        draw_in_window(left_player, right_player, LEFT_player_bullets, RIGHT_player_bullets, right_player_health,
                       left_player_health)
    main()


if __name__ == "__main__":
    main()
