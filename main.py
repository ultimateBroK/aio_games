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
        pygame.display.set_caption("Game Launcher")
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        
        # Initialize effects
        self.background = Background(self.WIDTH, self.HEIGHT)
        self.transition = None
        self.preview = GamePreview(self.WIDTH, self.HEIGHT)
        self.current_game = None
        self.selected_game = None

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        
        # Draw animated background
        self.background.update()
        self.background.draw(self.screen)
        
        # Title
        title = self.font.render("Choose a Game", True, (255, 255, 255))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 100))
        
        # Game options
        games = [
            ("1. Snake Game", SnakeGame),
            ("2. Hangman", HangmanGame),
            ("3. Pong vs AI", PongGame),
            ("4. Tetris", TetrisGame),
            ("Q. Quit", None)
        ]
        
        start_y = 250
        spacing = 60
        for i, (text, game) in enumerate(games):
            game_text = self.small_font.render(text, True, (255, 255, 255))
            text_pos = (self.WIDTH//2 - game_text.get_width()//2, start_y + i * spacing)
            self.screen.blit(game_text, text_pos)
            
            # Draw preview for selected game
            if game and text == self.selected_game:
                preview_pos = (self.WIDTH//2 + 150, start_y + i * spacing - 50)
                self.preview.draw(self.screen, text[3:], preview_pos)
        
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
                    if not self.transition:  # Only handle input when not transitioning
                        if event.key == pygame.K_1:
                            self.selected_game = "1. Snake Game"
                            self.start_transition(SnakeGame)
                        elif event.key == pygame.K_2:
                            self.selected_game = "2. Hangman"
                            self.start_transition(HangmanGame)
                        elif event.key == pygame.K_3:
                            self.selected_game = "3. Pong vs AI"
                            self.start_transition(PongGame)
                        elif event.key == pygame.K_4:
                            self.selected_game = "4. Tetris"
                            self.start_transition(TetrisGame)
                        elif event.key == pygame.K_q:
                            running = False
                elif event.type == pygame.MOUSEMOTION:
                    # Update preview on hover
                    mouse_y = event.pos[1]
                    start_y = 250
                    spacing = 60
                    for i, (text, _) in enumerate([
                        ("1. Snake Game", SnakeGame),
                        ("2. Hangman", HangmanGame),
                        ("3. Pong vs AI", PongGame),
                        ("4. Tetris", TetrisGame),
                        ("Q. Quit", None)
                    ]):
                        if start_y + i * spacing - 20 <= mouse_y <= start_y + i * spacing + 20:
                            self.selected_game = text
                            break
            
            # Update and handle transition
            if self.transition:
                self.transition.update()
                if self.transition.is_done():
                    if self.transition.fading_out:
                        # Start game
                        game = self.current_game()
                        self.transition.fading_out = False
                        game.run()
                        pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                    else:
                        # Return to menu
                        self.transition = None
                        self.current_game = None
            
            self.draw_menu()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run() 