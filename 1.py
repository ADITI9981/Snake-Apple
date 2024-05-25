import random
import pygame
import time
from pygame.locals import *

size = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, screen):
        self.image = pygame.image.load(r"C:\Users\DELL\Downloads\red_apple.jpg").convert()
        self.screen = screen
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(0, 24) * size
        self.y = random.randint(0, 19) * size

class Snake:
    def __init__(self, screen, length):
        self.length = length
        self.screen = screen
        self.block = pygame.image.load(r"C:\Users\DELL\Downloads\yellow.jpg").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw_block(self):
        self.screen.fill((32, 59, 39))
        for i in range(self.length):
            self.screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'
    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'
    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'
    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def crawling(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size

        self.draw_block()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple")
        pygame.mixer.init()
        sound = pygame.mixer.Sound(r"C:\Users\DELL\Downloads\tada-sound\Tada-sound.mp3")
        self.play_background_music()
        pygame.mixer.Sound.play(sound)
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((87, 249, 177))
        self.snake = Snake(self.surface, 1)
        self.snake.draw_block()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load(r"C:\Users\DELL\Downloads\positive-funny-background-music-for-video-games\positive-funny-background-music-for-video-games.mp3")
        pygame.mixer.music.play()

    def play(self):
        self.snake.crawling()
        self.apple.draw()
        self.score()
        pygame.display.flip()
        # Snake collision with apple
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound(r"C:\Users\DELL\Downloads\small-hand-bell-ding-sound-effect\small-hand-bell-ding-sound-effect.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        # Snake collision with itself
        for i in range(1, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound(r"C:\Users\DELL\Downloads\fail-and-game-over-sound-effect\fail-and-game-over-sound-effect.mp3")
                pygame.mixer.Sound.play(sound)
                raise Exception("Game Over")

    def game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your Score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To Play Again Press Enter, To Exit Press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        self.reset()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            if not pause:
                try:
                    self.play()
                except Exception as e:
                    self.game_over()
                    pause = True

            time.sleep(0.2)

if __name__ == "__main__":
    game = Game()
    game.run()
