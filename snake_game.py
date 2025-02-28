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

# Warna-warna cerah
LIME_GREEN = (50, 255, 50)
BRIGHT_BLUE = (0, 191, 255)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class SnakeGame:
    def __init__(self):
        # Inisialisasi layar
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Uler Kadut")
        self.clock = pygame.time.Clock()
        
        # Font
        self.font = pygame.font.Font(None, 36)
        
        # Variabel permainan
        self.reset_game()
        
        # Load high score
        self.load_high_score()
    
    def reset_game(self):
        # Posisi awal ular
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Awal bergerak ke kanan
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
    
    def spawn_food(self):
        while True:
            food_pos = (random.randint(0, GRID_WIDTH-1), 
                        random.randint(0, GRID_HEIGHT-1))
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
        # Kepala ular
        head = self.snake[0]
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH, 
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        
        # Cek tabrak diri sendiri
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Tambahkan kepala baru
        self.snake.insert(0, new_head)
        
        # Cek makanan
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            # Hapus ekor jika tidak memakan makanan
            self.snake.pop()
    
    def draw(self):
        # Bersihkan layar dengan warna cerah
        self.screen.fill(BRIGHT_BLUE)
        
        # Gambar ular
        for segment in self.snake:
            rect = pygame.Rect(
                segment[0] * GRID_SIZE, 
                segment[1] * GRID_SIZE, 
                GRID_SIZE-1, GRID_SIZE-1
            )
            pygame.draw.rect(self.screen, LIME_GREEN, rect)
        
        # Gambar makanan
        food_rect = pygame.Rect(
            self.food[0] * GRID_SIZE, 
            self.food[1] * GRID_SIZE, 
            GRID_SIZE-1, GRID_SIZE-1
        )
        pygame.draw.rect(self.screen, ORANGE, food_rect)
        
        # Tampilkan skor
        score_text = self.font.render(f"Score: {self.score}", True, PINK)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 50))
        
        # Update layar
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # Kontrol dengan panah dan WASD
                if event.key in [pygame.K_UP, pygame.K_w] and self.direction != (0, 1):
                    self.direction = (0, -1)
                elif event.key in [pygame.K_DOWN, pygame.K_s] and self.direction != (0, -1):
                    self.direction = (0, 1)
                elif event.key in [pygame.K_LEFT, pygame.K_a] and self.direction != (1, 0):
                    self.direction = (-1, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and self.direction != (-1, 0):
                    self.direction = (1, 0)
                
                # Restart game jika game over
                if self.game_over and event.key == pygame.K_SPACE:
                    self.save_high_score()
                    self.reset_game()
        
        return True
    
    def run(self):
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            if not self.game_over:
                # Gerakkan ular
                self.move_snake()
            
            # Gambar
            self.draw()
            
            # Game over
            if self.game_over:
                game_over_text = self.font.render("Game Over! Press SPACE to Restart", True, PINK)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(game_over_text, text_rect)
                pygame.display.flip()
            
            # Kontrol kecepatan
            self.clock.tick(50)
        
        # Simpan high score sebelum keluar
        self.save_high_score()
        pygame.quit()

# Jalankan game
if __name__ == "__main__":
    game = SnakeGame()
    game.run()