import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# display
screen_width = 600
screen_height = 600
gamewindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sougoto's Snake Game")  # Game Title

# BGI
bgi_wc = pygame.image.load('Bgi02.jpg')
bgi_wc = pygame.transform.scale(
    bgi_wc, (screen_width, screen_height)).convert_alpha()
bgi_ps = pygame.image.load('Bgi.jpg')
bgi_ps = pygame.transform.scale(
    bgi_ps, (screen_width, screen_height)).convert_alpha()
bgi_go = pygame.image.load('Bgi01.jpg')
bgi_go = pygame.transform.scale(
    bgi_go, (screen_width, screen_height)).convert_alpha()

# colors
white = (255, 255, 255)
cyan = (0, 255, 255)
blue = (173, 216, 230)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 173, 67)

# clock, font and fps
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
FPS = 30  # the number of consecutive full-screen images that are displayed per second


def text_screen(gamewindow, text, color, font, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])  # To update the screen with the text


def plot_snake(gamewindow, color, snake_list, snake_size):
    for snk in snake_list:
        pygame.draw.rect(gamewindow, color, [
                         snk[0], snk[1], snake_size, snake_size])


def welcome():
    gamewindow.blit(bgi_wc, (0, 0))
    play('wc.mp3')
    exit_game = False
    # welcome screen loop
    while (not exit_game):
        text_screen(gamewindow, "Welcome To Snakes", white, font, 160, 300)
        text_screen(gamewindow, "Press Space To Play", white, font, 160, 330)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    exit_game = True
                    play('Music_bgm.mp3')
                    playgame()
        pygame.display.update()
        clock.tick(FPS)


def play(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()


def playgame():
    with open("High Score.txt", "r") as f:
        highscore = int(f.read())
        f.close()
    # game specific variables
    game_over = False
    exit_game = False
    score = 0
    snake_x = 45
    snake_y = 55
    snake_size = 25
    snake_length = 1
    velocity_x = 0
    velocity_y = 0
    speed = 10
    apple_x = random.randint(50, screen_width - 50)
    apple_y = random.randint(50, screen_height - 50)
    apple_size = 20
    snake_list = [[snake_x, snake_y]]  # snake_x, snake_y -> coordinate of head

    # game loop
    while (not exit_game):  # the code inside while is equivalent to one frame
        if (game_over):
            gamewindow.blit(bgi_go, (0, 0))
            text_screen(
                gamewindow, "GAME OVER! PRESS ENTER TO CONTINUE", white, font, 5, 300)
            if (score > highscore):
                text_screen(gamewindow, "NEW HIGH SCORE: " +
                            str(score), white, font, 160, 340)
                with open("High Score.txt", "w") as f:
                    f.write(str(score))
                    f.close()
            else:
                text_screen(gamewindow, "SCORE: " +
                            str(score), white, font, 230, 340)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    exit_game = True
                elif (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_RETURN):
                        welcome()
                        # after playing the game we have to exit
                        exit_game = True
        else:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    exit_game = True
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_RIGHT):
                        velocity_x = speed
                        velocity_y = 0
                    elif (event.key == pygame.K_LEFT):
                        velocity_x = -speed
                        velocity_y = 0
                    elif (event.key == pygame.K_UP):
                        velocity_y = -speed
                        velocity_x = 0
                    elif (event.key == pygame.K_DOWN):
                        velocity_y = speed
                        velocity_x = 0
            snake_x += velocity_x
            snake_y += velocity_y
            if (snake_x <= 4 or snake_x >= 570):
                play('gameover.mp3')
                game_over = True
            elif (snake_y <= 4 or snake_y >= 570):
                play('gameover.mp3')
                game_over = True
            for i in range(0, snake_length - 1):
                if (snake_list[-1] == snake_list[i]):
                    play('gameover.mp3')
                    game_over = True
                    break
            if (abs(snake_x - apple_x) <= 20 and abs(snake_y - apple_y) <= 20):
                score += 5
                snake_length += 1
                apple_x = random.randint(50, screen_width - 50)
                apple_y = random.randint(50, screen_height - 50)
            gamewindow.blit(bgi_ps, (0, 0))
            text_screen(gamewindow, "SCORE: " + str(score), red, font, 10, 10)
            snake_list.append([snake_x, snake_y])
            if (len(snake_list) > snake_length):
                del snake_list[0]
            plot_snake(gamewindow, black, snake_list, snake_size)
            pygame.draw.rect(gamewindow, red, [
                apple_x, apple_y, apple_size, apple_size])
            plot_snake(gamewindow, black, snake_list, snake_size)
        pygame.display.update()  # To show the changes made by you
        clock.tick(FPS)


# checking wheather our highscore.txt file exsits or not
if (not os.path.exists("High Score.txt")):
    with open("High Score.txt", "w") as f:
        f.write("0")
        f.close()
welcome()
pygame.quit()
quit()
