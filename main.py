import pygame
import sys
from games import SnakeGame, HangmanGame, PongGame

class GameLauncher:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Launcher")
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        
        # Title
        title = self.font.render("Choose a Game", True, (255, 255, 255))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 100))
        
        # Game options
        snake_text = self.small_font.render("1. Snake Game", True, (255, 255, 255))
        hangman_text = self.small_font.render("2. Hangman", True, (255, 255, 255))
        pong_text = self.small_font.render("3. Pong", True, (255, 255, 255))
        quit_text = self.small_font.render("Q. Quit", True, (255, 255, 255))
        
        self.screen.blit(snake_text, (self.WIDTH//2 - snake_text.get_width()//2, 250))
        self.screen.blit(hangman_text, (self.WIDTH//2 - hangman_text.get_width()//2, 300))
        self.screen.blit(pong_text, (self.WIDTH//2 - pong_text.get_width()//2, 350))
        self.screen.blit(quit_text, (self.WIDTH//2 - quit_text.get_width()//2, 450))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game = SnakeGame()
                        game.run()
                        pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Reset display
                    elif event.key == pygame.K_2:
                        game = HangmanGame()
                        game.run()
                        pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Reset display
                    elif event.key == pygame.K_3:
                        game = PongGame()
                        game.run()
                        pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Reset display
                    elif event.key == pygame.K_q:
                        running = False
            
            self.draw_menu()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run() 