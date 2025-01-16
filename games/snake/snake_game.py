import pygame
import sys
import random

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.GRID_SIZE = 20
        self.SCORE_HEIGHT = 100  # Chiều cao khu vực điểm số
        self.GRID_WIDTH = self.WIDTH // self.GRID_SIZE  # Số ô theo chiều ngang
        self.GRID_HEIGHT = (self.HEIGHT - self.SCORE_HEIGHT) // self.GRID_SIZE  # Số ô theo chiều dọc
        self.PLAY_AREA_WIDTH = self.WIDTH
        self.PLAY_AREA_HEIGHT = self.HEIGHT - self.SCORE_HEIGHT
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (50, 50, 50)
        
        self.reset_game()
        
    def reset_game(self):
        self.snake = [(self.GRID_WIDTH//2, self.GRID_HEIGHT//2)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        
    def spawn_food(self):
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
                
    def draw_grid(self):
        # Draw vertical lines
        for x in range(self.GRID_WIDTH + 1):
            pygame.draw.line(self.screen, self.DARK_GRAY,
                           (x * self.GRID_SIZE, 0),
                           (x * self.GRID_SIZE, self.PLAY_AREA_HEIGHT))
        # Draw horizontal lines
        for y in range(self.GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, self.DARK_GRAY,
                           (0, y * self.GRID_SIZE),
                           (self.PLAY_AREA_WIDTH, y * self.GRID_SIZE))
                
    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Draw grid
        self.draw_grid()
        
        # Draw snake
        for segment in self.snake:
            x, y = segment
            pygame.draw.rect(self.screen, self.GREEN,
                           (x * self.GRID_SIZE + 1, y * self.GRID_SIZE + 1,
                            self.GRID_SIZE - 2, self.GRID_SIZE - 2))
            
        # Draw food
        pygame.draw.rect(self.screen, self.RED,
                        (self.food[0] * self.GRID_SIZE + 1,
                         self.food[1] * self.GRID_SIZE + 1,
                         self.GRID_SIZE - 2, self.GRID_SIZE - 2))
        
        # Draw score area background
        pygame.draw.rect(self.screen, self.BLACK,
                        (0, self.PLAY_AREA_HEIGHT, self.WIDTH, self.SCORE_HEIGHT))
        pygame.draw.line(self.screen, self.WHITE,
                        (0, self.PLAY_AREA_HEIGHT),
                        (self.WIDTH, self.PLAY_AREA_HEIGHT), 2)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, 
                        (self.WIDTH//2 - score_text.get_width()//2,
                         self.PLAY_AREA_HEIGHT + 20))
        
        # Draw controls hint
        controls = self.small_font.render("Arrow Keys - Move    ESC - Menu", 
                                        True, self.GRAY)
        self.screen.blit(controls, 
                        (self.WIDTH//2 - controls.get_width()//2,
                         self.HEIGHT - 40))
        
        if self.game_over:
            # Create semi-transparent overlay
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.fill(self.BLACK)
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            
            # Create message box
            box_width = 400
            box_height = 160
            box_x = self.WIDTH//2 - box_width//2
            box_y = self.HEIGHT//2 - box_height//2
            
            # Draw box background and border
            pygame.draw.rect(self.screen, self.GRAY, 
                           (box_x, box_y, box_width, box_height))
            pygame.draw.rect(self.screen, self.WHITE, 
                           (box_x, box_y, box_width, box_height), 3)
            
            # Draw game over message
            text = self.font.render("Game Over!", True, self.RED)
            score_text = self.small_font.render(f"Final Score: {self.score}", 
                                              True, self.WHITE)
            restart = self.small_font.render("SPACE - Play again    ESC - Menu", 
                                           True, self.WHITE)
            
            self.screen.blit(text, 
                            (self.WIDTH//2 - text.get_width()//2, box_y + 30))
            self.screen.blit(score_text, 
                            (self.WIDTH//2 - score_text.get_width()//2, box_y + 80))
            self.screen.blit(restart, 
                            (self.WIDTH//2 - restart.get_width()//2, box_y + 120))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Return to main menu
                    elif not self.game_over:
                        if event.key == pygame.K_UP and self.direction != (0, 1):
                            self.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.direction = (1, 0)
                    elif event.key == pygame.K_SPACE:
                        self.reset_game()
            
            if not self.game_over:
                # Move snake
                head = self.snake[0]
                new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
                
                # Handle wall crossing
                new_head = ((new_head[0] + self.GRID_WIDTH) % self.GRID_WIDTH,
                           (new_head[1] + self.GRID_HEIGHT) % self.GRID_HEIGHT)
                
                # Check for collisions with self
                if new_head in self.snake:
                    self.game_over = True
                else:
                    self.snake.insert(0, new_head)
                    if new_head == self.food:
                        self.score += 1
                        self.food = self.spawn_food()
                    else:
                        self.snake.pop()
            
            self.draw()
            self.clock.tick(10)  # Control game speed

def main():
    # Only initialize the game without running
    return SnakeGame()

if __name__ == "__main__":
    # When running this file directly, show message
    print("Please run the game from the main menu (main.py)") 