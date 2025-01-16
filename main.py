import pygame
import sys
from games import SnakeGame, HangmanGame, PongGame, TetrisGame
from games.utils.effects import Background, Transition, GamePreview

class GameLauncher:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Python Arcade Collection")
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.tiny_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        
        # Initialize effects
        self.background = Background(self.WIDTH, self.HEIGHT)
        self.transition = None
        self.preview = GamePreview(self.WIDTH, self.HEIGHT)
        self.current_game = None
        self.selected_index = 0
        self.games = [
            ("Snake Game", SnakeGame),
            ("Hangman", HangmanGame),
            ("Pong", PongGame),
            ("Tetris", TetrisGame)
        ]

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        
        # Draw animated background
        self.background.update()
        self.background.draw(self.screen)
        
        # Title
        title = self.font.render("Python Arcade Collection", True, (255, 255, 255))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 100))
        
        # Game options
        start_y = 250
        spacing = 60
        for i, (text, game) in enumerate(self.games):
            color = (255, 255, 255) if i == self.selected_index else (128, 128, 128)
            game_text = self.small_font.render(text, True, color)
            text_pos = (self.WIDTH//2 - game_text.get_width()//2, start_y + i * spacing)
            self.screen.blit(game_text, text_pos)
            
            # Draw preview for selected game
            if i == self.selected_index:
                preview_pos = (self.WIDTH//2 + 150, start_y + i * spacing - 50)
                self.preview.draw(self.screen, text, preview_pos)
        
        # Draw quit text in bottom right corner
        quit_text = self.tiny_font.render("Ctrl+Q to Quit", True, (128, 128, 128))
        self.screen.blit(quit_text, (self.WIDTH - quit_text.get_width() - 20, self.HEIGHT - 30))
        
        # Draw navigation hint with arrow symbols
        nav_text = self.tiny_font.render("Use arrow key UP-DOWN to navigate", True, (128, 128, 128))
        self.screen.blit(nav_text, (20, self.HEIGHT - 30))
        
        # Draw transition effect if active
        if self.transition:
            self.transition.draw(self.screen)
        
        pygame.display.flip()

    def start_transition(self, game_class):
        self.transition = Transition(self.WIDTH, self.HEIGHT)
        self.current_game = game_class

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Handle Ctrl+Q for quitting only in main menu
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if self.transition is None:  # Only quit if not in transition
                            running = False
                    elif not self.transition:  # Only handle input when not transitioning
                        if event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % len(self.games)
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % len(self.games)
                        elif event.key == pygame.K_RETURN:
                            _, game_class = self.games[self.selected_index]
                            self.start_transition(game_class)
            
            # Update and handle transition
            if self.transition:
                self.transition.update()
                if self.transition.is_done():
                    if self.transition.fading_out:
                        # Start game
                        game = self.current_game()
                        self.transition.fading_out = False
                        try:
                            game.run()
                        except Exception as e:
                            print(f"Game error: {e}")
                        finally:
                            pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                    else:
                        # Return to menu
                        self.transition = None
                        self.current_game = None
            
            try:
                self.draw_menu()
            except pygame.error:
                # Reinitialize display if it was quit
                self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                pygame.display.set_caption("Python Arcade Collection")
                continue
                
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run() 