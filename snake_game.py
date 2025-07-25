import pygame
import random
import json
import os

# Inisialisasi Pygame
pygame.init()

# Pengaturan Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Warna
LIME_GREEN = (50, 255, 50)
BRIGHT_BLUE = (0, 191, 255)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (30, 30, 30)

class Button:
    def __init__(self, text, x, y, width, height, base_color, hover_color, font, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.font = font
        self.action = action

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            r = self.current_color[0] + (self.hover_color[0] - self.current_color[0]) // 5
            g = self.current_color[1] + (self.hover_color[1] - self.current_color[1]) // 5
            b = self.current_color[2] + (self.hover_color[2] - self.current_color[2]) // 5
            self.current_color = (r, g, b)
        else:
            r = self.current_color[0] + (self.base_color[0] - self.current_color[0]) // 5
            g = self.current_color[1] + (self.base_color[1] - self.current_color[1]) // 5
            b = self.current_color[2] + (self.base_color[2] - self.current_color[2]) // 5
            self.current_color = (r, g, b)

        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Uler Kadut")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.load_high_score()
        self.difficulty = 10
        self.state = "menu"
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food_pos not in self.snake:
                return food_pos

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

    def move_snake(self):
        head = self.snake[0]
        new_head = ((head[0] + self.direction[0]) % GRID_WIDTH, (head[1] + self.direction[1]) % GRID_HEIGHT)
        if new_head in self.snake:
            self.game_over = True
            return
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw_game(self):
        self.screen.fill(BRIGHT_BLUE)
        for segment in self.snake:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(self.screen, LIME_GREEN, rect)
        food_rect = pygame.Rect(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(self.screen, ORANGE, food_rect)
        score_text = self.font.render(f"Score: {self.score}", True, PINK)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 50))
        if self.game_over:
            game_over_text = self.font.render("Game Over! Press SPACE or Click to Restart", True, PINK)
            rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, rect)
        pygame.display.flip()

    def main_menu(self):
        play_button = Button("Play", 300, 200, 200, 60, PINK, WHITE, self.font, action="play")
        diff_button = Button("Difficulty", 300, 280, 200, 60, ORANGE, WHITE, self.font, action="difficulty")
        quit_button = Button("Quit", 300, 360, 200, 60, LIME_GREEN, WHITE, self.font, action="quit")
        buttons = [play_button, diff_button, quit_button]

        while self.state == "menu":
            self.screen.fill(DARK_GREY)
            title = self.large_font.render("Uler Kadut", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True

            for button in buttons:
                button.draw(self.screen, mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    if button.action == "play":
                        self.reset_game()
                        self.state = "game"
                    elif button.action == "difficulty":
                        self.state = "difficulty"
                    elif button.action == "quit":
                        self.state = "quit"

            pygame.display.flip()
            self.clock.tick(60)

    def difficulty_menu(self):
        easy = Button("Easy", 300, 200, 200, 60, LIME_GREEN, WHITE, self.font, action=5)
        medium = Button("Medium", 300, 280, 200, 60, ORANGE, WHITE, self.font, action=10)
        hard = Button("Hard", 300, 360, 200, 60, PINK, WHITE, self.font, action=20)
        back = Button("Back", 300, 440, 200, 60, BRIGHT_BLUE, WHITE, self.font, action="back")
        buttons = [easy, medium, hard, back]

        while self.state == "difficulty":
            self.screen.fill(DARK_GREY)
            title = self.large_font.render("Select Difficulty", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True

            for button in buttons:
                button.draw(self.screen, mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    if button.action == "back":
                        self.state = "menu"
                    else:
                        self.difficulty = button.action
                        self.state = "menu"

            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        while self.state != "quit":
            if self.state == "menu":
                self.main_menu()
            elif self.state == "difficulty":
                self.difficulty_menu()
            elif self.state == "game":
                running = True
                while running and self.state == "game":
                    mouse_click = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            self.state = "quit"
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP and self.direction != (0, 1):
                                self.direction = (0, -1)
                            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                                self.direction = (0, 1)
                            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                                self.direction = (-1, 0)
                            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                                self.direction = (1, 0)
                            elif event.key == pygame.K_SPACE and self.game_over:
                                self.save_high_score()
                                self.reset_game()
                            elif event.key == pygame.K_ESCAPE:
                                self.state = "menu"
                        if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                            self.save_high_score()
                            self.reset_game()

                    if not self.game_over:
                        self.move_snake()
                    self.draw_game()
                    self.clock.tick(self.difficulty)
        self.save_high_score()
        pygame.quit()

if __name__ == "__main__":
    SnakeGame().run()