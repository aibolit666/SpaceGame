import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('First game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 0)
GREEN = (0, 255, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/laser.wav')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
UFO_WIDTH, UFO_HEIGHT = 55, 40

UFO1_HIT = pygame.USEREVENT + 1
UFO2_HIT = pygame.USEREVENT + 2

UFO_1_IMAGE = pygame.image.load(
    os.path.join('Assets', 'ufo.png'))
UFO_1 = pygame.transform.scale(UFO_1_IMAGE, (UFO_WIDTH, UFO_HEIGHT))
UFO_2_IMAGE = pygame.image.load(
    os.path.join('Assets', 'ufo2.png'))
UFO_2 = pygame.transform.scale(UFO_2_IMAGE, (UFO_WIDTH, UFO_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.jpg')), (WIDTH, HEIGHT))


def draw_window(ufo1, ufo2, ufo1_bullets, ufo2_bullets, ufo1_health, ufo2_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    ufo2_health_text = HEALTH_FONT.render("Health: " + str(ufo2_health), 1, WHITE)
    ufo1_health_text = HEALTH_FONT.render("Health: " + str(ufo1_health), 1, WHITE)
    WIN.blit(ufo2_health_text, (WIDTH - ufo2_health_text.get_width() - 10, 10))
    WIN.blit(ufo1_health_text, (10, 10))

    WIN.blit(UFO_1, (ufo1.x, ufo1.y))
    WIN.blit(UFO_2, (ufo2.x, ufo2.y))

    for bullet in ufo2_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    for bullet in ufo1_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def ufo1_handle_movement(keys_pressed, ufo1):
    if keys_pressed[pygame.K_a] and ufo1.x - VEL > 0:  # LEFT
        ufo1.x -= VEL
    if keys_pressed[pygame.K_d] and ufo1.x + VEL < BORDER.x - ufo1.width:  # RIGHT
        ufo1.x += VEL
    if keys_pressed[pygame.K_w] and ufo1.y - VEL > 0:  # UP
        ufo1.y -= VEL
    if keys_pressed[pygame.K_s] and ufo1.y + VEL < HEIGHT - ufo1.height:  # DOWN
        ufo1.y += VEL


def ufo2_handle_movement(keys_pressed, ufo2):
    if keys_pressed[pygame.K_LEFT] and ufo2.x - VEL > BORDER.x + BORDER.width:  # LEFT
        ufo2.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and ufo2.x + VEL < WIDTH - ufo2.width:  # RIGHT
        ufo2.x += VEL
    if keys_pressed[pygame.K_UP] and ufo2.y - VEL > 0:  # UP
        ufo2.y -= VEL
    if keys_pressed[pygame.K_DOWN] and ufo2.y + VEL < HEIGHT - ufo2.height:  # DOWN
        ufo2.y += VEL


def handle_bullets(ufo1_bullets, ufo2_bullets, ufo1, ufo2):
    for bullet in ufo1_bullets:
        bullet.x += BULLET_VEL
        if ufo2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(UFO2_HIT))
            ufo1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            ufo1_bullets.remove(bullet)

    for bullet in ufo2_bullets:
        bullet.x -= BULLET_VEL
        if ufo1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(UFO1_HIT))
            ufo2_bullets.remove(bullet)
        elif bullet.x < 0:
            ufo2_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    ufo1 = pygame.Rect(100, 300, UFO_WIDTH, UFO_HEIGHT)
    ufo2 = pygame.Rect(700, 300, UFO_WIDTH, UFO_HEIGHT)

    ufo1_bullets = []
    ufo2_bullets = []

    ufo1_health = 10
    ufo2_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(ufo1_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        ufo1.x + ufo1.width, ufo1.y + ufo1.height//2 - 2, 10, 5)  # Start position of a bullet
                    ufo1_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(ufo2_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        ufo2.x, ufo2.y + ufo2.height//2 - 2, 10, 5)  # Start position of a bullet
                    ufo2_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == UFO2_HIT:
                ufo2_health -= 1
                x = random.randint(1, 10)
                BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/' + str(x) + '.wav')
                BULLET_HIT_SOUND.play()

            if event.type == UFO1_HIT:
                ufo1_health -= 1
                x = random.randint(1, 10)
                BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/' + str(x) + '.wav')
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if ufo2_health <= 0:
            winner_text = "UFO 1 WINS!"
        if ufo1_health <= 0:
            winner_text = "UFO 2 WINS!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        ufo1_handle_movement(keys_pressed, ufo1)
        ufo2_handle_movement(keys_pressed, ufo2)

        handle_bullets(ufo1_bullets, ufo2_bullets, ufo1, ufo2)

        draw_window(ufo1, ufo2, ufo1_bullets, ufo2_bullets, ufo1_health, ufo2_health)

    main()


if __name__ == "__main__":
    main()
