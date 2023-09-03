import pygame
import random

pygame.init()
pygame.font.init()

name_of_game = 'Ping Pong'
width_window = 800
height_window = 480


white = (255,255,255)
black = (0,0,0)

Fps = 60

platform_width = 100
platform_height = 10
platform_speed = 10
platform_position = pygame.rect.Rect(width_window / 2 - platform_width / 2, height_window - platform_height * 2,
                                     platform_width, platform_height)

circle_first_interact = False
circle_radius = 10
circle_speed = 7
circle_speed_x = 0
circle_speed_y = circle_speed
circle_posisition = pygame.rect.Rect(width_window / 2 - circle_radius, height_window / 2 - circle_radius,
                                     circle_radius * 2, circle_radius * 2)

score = 0
font_path = pygame.font.match_font('arial')
font_size_score = pygame.font.Font(font_path, 35)
font_size_restart = pygame.font.Font(font_path, 30)

screen = pygame.display.set_mode([width_window, height_window])
pygame.display.set_caption(name_of_game)

freezing = pygame.time.Clock()

game_over = False

working = True
while working:
    for a in pygame.event.get():
        if a.type == pygame.QUIT:
            working = False
            continue
        elif a.type == pygame.KEYDOWN:
            if a.key == pygame.K_ESCAPE:
                working = False
                continue
            elif a.key == pygame.K_r:
                game_over = False

                platform_position.centerx = width_window / 2
                platform_position.bottom = height_window - platform_height

                circle_posisition.center = [width_window / 2, height_window / 2]
                circle_speed_x = 0
                circle_speed_y = circle_speed
                circle_first_interact = False

                score = 0

    screen.fill(black)
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            platform_position.x -= platform_speed
        if keys[pygame.K_d]:
            platform_position.x += platform_speed

        if platform_position.colliderect(circle_posisition):
            if not circle_first_interact:
                if random.randint(0, 1) == 0:
                    circle_speed_x = circle_speed
                else:
                    circle_speed_x = -circle_speed
                circle_first_interact = True
            circle_speed_y = -circle_speed
            score += 1

        pygame.draw.rect(screen, white, platform_position)

    circle_posisition.x += circle_speed_x
    circle_posisition.y += circle_speed_y

    if circle_posisition.bottom >= height_window:
        game_over = True
        circle_speed_y = -circle_speed
    elif circle_posisition.top <= 0:
        circle_speed_y = circle_speed
    elif circle_posisition.left <= 0:
        circle_speed_x = circle_speed
    elif circle_posisition.right >= width_window:
        circle_speed_x = -circle_speed

    pygame.draw.circle(screen, white, circle_posisition.center, circle_radius)

    surface_score = font_size_score.render(str(score), False, white)
    if not game_over:
        screen.blit(surface_score, [width_window / 2 - surface_score.get_width() / 2, 15])
    else:
        retry = font_size_restart.render('Нажмите R, чтобы перезапустить', True, white)
        screen.blit(surface_score, [width_window / 2 - surface_score.get_width() / 2, height_window / 3])
        screen.blit(retry, [width_window / 2 - retry.get_width() / 2, height_window / 3  + surface_score.get_height()])

    freezing.tick(Fps)
    pygame.display.flip()

pygame.quit()