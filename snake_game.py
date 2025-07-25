import pygame
import random
import json

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
LIME_GREEN = (50, 255, 50)
BRIGHT_BLUE = (0, 191, 255)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Load sounds
EAT_SOUND = pygame.mixer.Sound("eat.wav")
GAME_OVER_SOUND = pygame.mixer.Sound("gameover.wav")
CLICK_SOUND = pygame.mixer.Sound("click.wav")

# Background music
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)

    def move(self):
        head = self.body[0]
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )

        if new_head in self.body:
            return False

        self.body.insert(0, new_head)
        return True

    def grow(self):
        pass  # do nothing because we keep the tail

    def shrink(self):
        self.body.pop()

    def set_direction(self, new_dir):
        if (new_dir[0] != -self.direction[0] or new_dir[1] != -self.direction[1]):
            self.direction = new_dir

    def get_head(self):
        return self.body[0]

class Food:
    def __init__(self, snake):
        self.position = self.spawn(snake)

    def spawn(self, snake):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake.body:
                return pos

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Uler Kadut")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.load_high_score()
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = 0
        self.game_over = False

    def load_high_score(self):
        try:
            with open('highscore.json', 'r') as f:
                self.high_score = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_score = 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('highscore.json', 'w') as f:
                json.dump(self.high_score, f)

    def update(self):
        alive = self.snake.move()
        if not alive:
            GAME_OVER_SOUND.play()
            self.game_over = True
            return

        if self.snake.get_head() == self.food.position:
            self.score += 1
            self.food = Food(self.snake)
            EAT_SOUND.play()
        else:
            self.snake.shrink()

    def draw(self):
        self.screen.fill(BRIGHT_BLUE)

        for segment in self.snake.body:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
            pygame.draw.rect(self.screen, LIME_GREEN, rect)

        food_rect = pygame.Rect(self.food.position[0] * GRID_SIZE, self.food.position[1] * GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
        pygame.draw.rect(self.screen, ORANGE, food_rect)

        score_text = self.font.render(f"Score: {self.score}", True, PINK)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 50))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                CLICK_SOUND.play()
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.snake.set_direction((0, -1))
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.snake.set_direction((0, 1))
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.snake.set_direction((-1, 0))
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.snake.set_direction((1, 0))
                elif self.game_over and event.key == pygame.K_SPACE:
                    self.save_high_score()
                    self.reset_game()
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()

            if not self.game_over:
                self.update()

            self.draw()

            if self.game_over:
                game_over_text = self.font.render("Game Over! Press SPACE to Restart", True, PINK)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(game_over_text, text_rect)
                pygame.display.flip()

            self.clock.tick(15)

        self.save_high_score()
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
