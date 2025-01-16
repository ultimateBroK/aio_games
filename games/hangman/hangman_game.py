import random
import pygame
import sys

class HangmanGame:
    # Game constants
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    WORDS = ['ant', 'baboon', 'badger', 'bat', 'bear', 'beaver', 'camel', 'cat', 'clam', 'cobra',
             'cougar', 'coyote', 'crow', 'deer', 'dog', 'donkey', 'duck', 'eagle', 'ferret', 'fox',
             'frog', 'goat', 'goose', 'hawk', 'lion', 'lizard', 'llama', 'monkey', 'moose', 'mouse',
             'mule', 'newt', 'otter', 'owl', 'panda', 'parrot', 'pigeon', 'python', 'rabbit', 'ram',
             'rat', 'raven', 'rhino', 'salmon', 'seal', 'shark', 'sheep', 'skunk', 'sloth', 'snake',
             'spider', 'stork', 'swan', 'tiger', 'toad', 'trout', 'turkey', 'turtle', 'whale', 'wolf']

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hangman")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.running = True

    def reset_game(self):
        self.secret_word = random.choice(self.WORDS)
        self.missed_letters = ''
        self.correct_letters = ''
        self.game_is_done = False

    def draw_hangman(self):
        # Draw gallows
        pygame.draw.line(self.screen, self.WHITE, (100, 500), (300, 500), 3)  # base
        pygame.draw.line(self.screen, self.WHITE, (200, 500), (200, 100), 3)  # pole
        pygame.draw.line(self.screen, self.WHITE, (200, 100), (300, 100), 3)  # top
        pygame.draw.line(self.screen, self.WHITE, (300, 100), (300, 150), 3)  # rope

        # Draw hangman based on missed letters
        if len(self.missed_letters) >= 1:
            pygame.draw.circle(self.screen, self.WHITE, (300, 180), 30)  # head
        if len(self.missed_letters) >= 2:
            pygame.draw.line(self.screen, self.WHITE, (300, 210), (300, 350), 3)  # body
        if len(self.missed_letters) >= 3:
            pygame.draw.line(self.screen, self.WHITE, (300, 260), (250, 300), 3)  # left arm
        if len(self.missed_letters) >= 4:
            pygame.draw.line(self.screen, self.WHITE, (300, 260), (350, 300), 3)  # right arm
        if len(self.missed_letters) >= 5:
            pygame.draw.line(self.screen, self.WHITE, (300, 350), (250, 400), 3)  # left leg
        if len(self.missed_letters) >= 6:
            pygame.draw.line(self.screen, self.WHITE, (300, 350), (350, 400), 3)  # right leg

    def draw(self):
        self.screen.fill(self.BLACK)
        self.draw_hangman()

        # Draw word
        word_display = ''
        for letter in self.secret_word:
            if letter in self.correct_letters:
                word_display += letter + ' '
            else:
                word_display += '_ '
        word_text = self.font.render(word_display, True, self.WHITE)
        self.screen.blit(word_text, (400, 300))

        # Draw missed letters
        missed_text = self.font.render(f"Missed letters: {' '.join(self.missed_letters)}", True, self.WHITE)
        self.screen.blit(missed_text, (400, 200))

        # Draw game over message in bottom right
        if self.game_is_done:
            if len(self.missed_letters) >= 6:
                game_over_text = self.font.render(f"Game Over! Word: {self.secret_word}", True, self.WHITE)
            else:
                game_over_text = self.font.render("You won!", True, self.WHITE)
            self.screen.blit(game_over_text, (self.WIDTH - game_over_text.get_width() - 20, self.HEIGHT - 60))
            replay_text = self.small_font.render("Press SPACE to play again", True, self.WHITE)
            self.screen.blit(replay_text, (self.WIDTH - replay_text.get_width() - 20, self.HEIGHT - 30))

        # Draw back button
        back_text = self.small_font.render("Press ESC for menu", True, self.WHITE)
        self.screen.blit(back_text, (10, 10))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Back to menu
                    self.running = False
                    return True
                if event.key == pygame.K_SPACE and self.game_is_done:
                    self.reset_game()
                elif not self.game_is_done and event.unicode.isalpha():
                    guess = event.unicode.lower()
                    if guess not in self.missed_letters + self.correct_letters:
                        if guess in self.secret_word:
                            self.correct_letters += guess
                            # Check if won
                            won = all(letter in self.correct_letters for letter in self.secret_word)
                            if won:
                                self.game_is_done = True
                        else:
                            self.missed_letters += guess
                            if len(self.missed_letters) >= 6:
                                self.game_is_done = True
        return True

    def run(self):
        self.running = True
        while self.running:
            if not self.handle_events():
                pygame.quit()
                sys.exit()
            self.draw()
            self.clock.tick(self.FPS)

def main():
    game = HangmanGame()
    game.run()

if __name__ == "__main__":
    main() 