import pygame
import random
import math

class HangmanGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hangman")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        try:
            self.font = pygame.font.Font("games/fonts/Roboto-Bold.ttf", 48)
            self.small_font = pygame.font.Font("games/fonts/Roboto-Regular.ttf", 36)
            self.tiny_font = pygame.font.Font("games/fonts/Roboto-Light.ttf", 24)
        except:
            self.font = pygame.font.Font(None, 48)
            self.small_font = pygame.font.Font(None, 36)
            self.tiny_font = pygame.font.Font(None, 24)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 150, 255)
        
        # Animation variables
        self.menu_alpha = 0
        self.fade_speed = 5
        self.letter_animations = {}  # {letter: (scale, alpha)}
        self.hint_alpha = 0
        self.hint_showing = False
        
        # Game states
        self.MENU = 0
        self.PLAYING = 1
        self.state = self.MENU
        
        # Word categories and their words with hints
        self.categories = {
            "Animals": [
                ("ELEPHANT", "Largest land mammal with a trunk"),
                ("GIRAFFE", "Tallest animal with a long neck"),
                ("PENGUIN", "Flightless bird that swims well"),
                ("DOLPHIN", "Intelligent marine mammal"),
                ("KANGAROO", "Australian animal with a pouch"),
                ("CHEETAH", "Fastest land animal"),
                ("OCTOPUS", "Sea creature with eight arms"),
                ("BUTTERFLY", "Colorful flying insect"),
                ("RHINOCEROS", "Large animal with horns"),
                ("CROCODILE", "Reptile that lives in water"),
                ("PANDA", "Black and white bear from China"),
                ("GORILLA", "Large primate"),
                ("ZEBRA", "Striped African animal"),
                ("KOALA", "Australian tree-dwelling animal"),
                ("TIGER", "Large striped cat")
            ],
            "Crypto": [
                ("BITCOIN", "First and most popular cryptocurrency"),
                ("ETHEREUM", "Platform for smart contracts"),
                ("BLOCKCHAIN", "Decentralized ledger technology"),
                ("WALLET", "Stores digital assets"),
                ("MINING", "Process of validating transactions"),
                ("DEFI", "Decentralized finance"),
                ("TOKEN", "Digital asset on a blockchain"),
                ("ALTCOIN", "Alternative cryptocurrency"),
                ("LEDGER", "Record of transactions"),
                ("STAKING", "Holding coins to support network"),
                ("METAMASK", "Popular crypto wallet"),
                ("SOLANA", "Fast blockchain platform"),
                ("CARDANO", "Proof of stake blockchain"),
                ("BINANCE", "Major crypto exchange"),
                ("POLYGON", "Layer 2 scaling solution")
            ],
            "AI": [
                ("NEURAL", "Brain-inspired network"),
                ("LEARNING", "AI improving from experience"),
                ("DATASET", "Collection of training data"),
                ("ALGORITHM", "Step-by-step problem solving"),
                ("TENSOR", "Multi-dimensional array"),
                ("TRAINING", "Teaching AI models"),
                ("INFERENCE", "AI making predictions"),
                ("ROBOTICS", "Study of robots"),
                ("VISION", "Computer understanding images"),
                ("DEEPMIND", "Famous AI company"),
                ("PYTORCH", "Deep learning framework"),
                ("KERAS", "Neural network library"),
                ("TENSORFLOW", "Machine learning platform"),
                ("TRANSFORMER", "Attention-based model"),
                ("BERT", "Language understanding model")
            ],
            "LLMs": [
                ("CLAUDE", "Anthropic's AI assistant"),
                ("GPT", "Generative Pre-trained Transformer"),
                ("LLAMA", "Meta's language model"),
                ("MISTRAL", "Open source LLM"),
                ("GEMINI", "Google's multimodal AI"),
                ("PROMPT", "Input to guide AI response"),
                ("TOKENS", "Text units for processing"),
                ("CONTEXT", "Information window for AI"),
                ("EMBEDDING", "Vector representation"),
                ("ATTENTION", "Focus mechanism in AI"),
                ("DECODER", "Generates output text"),
                ("ENCODER", "Processes input text"),
                ("FINE", "Model specialization"),
                ("TUNING", "Adjusting model parameters"),
                ("ANTHROPIC", "AI safety company")
            ]
        }
        
        self.selected_category = 0
        self.category_list = list(self.categories.keys())
        self.used_words = {category: set() for category in self.categories}
        self.reset_game()
        
    def get_random_word(self, category):
        # Get list of unused words
        available_words = [(word, hint) for word, hint in self.categories[category] 
                         if word not in self.used_words[category]]
        
        # Reset if all words used
        if not available_words:
            self.used_words[category].clear()
            available_words = self.categories[category]
            
        word, hint = random.choice(available_words)
        self.used_words[category].add(word)
        return word, hint
        
    def reset_game(self):
        # Select random word from chosen category
        category = self.category_list[self.selected_category]
        self.word, self.hint = self.get_random_word(category)
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.game_over = False
        self.won = False
        self.letter_animations.clear()
        self.hint_alpha = 0
        self.hint_showing = False
        
    def is_word_guessed(self):
        return all(letter in self.guessed_letters for letter in self.word)
        
    def draw_hangman(self):
        # Draw gallows with smooth lines
        def draw_smooth_line(start, end, width=3):
            pygame.draw.line(self.screen, self.WHITE, start, end, width)
            pygame.draw.circle(self.screen, self.WHITE, start, width//2)
            pygame.draw.circle(self.screen, self.WHITE, end, width//2)
            
        # Base structure
        draw_smooth_line((100, 400), (300, 400))  # Base
        draw_smooth_line((200, 400), (200, 100))  # Pole
        draw_smooth_line((200, 100), (300, 100))  # Top
        draw_smooth_line((300, 100), (300, 150))  # Rope
        
        if self.wrong_guesses >= 1:
            # Head with smooth circle
            pygame.draw.circle(self.screen, self.WHITE, (300, 175), 25, 3)
        if self.wrong_guesses >= 2:
            # Body
            draw_smooth_line((300, 200), (300, 300))
        if self.wrong_guesses >= 3:
            # Left arm
            draw_smooth_line((300, 225), (250, 275))
        if self.wrong_guesses >= 4:
            # Right arm
            draw_smooth_line((300, 225), (350, 275))
        if self.wrong_guesses >= 5:
            # Left leg
            draw_smooth_line((300, 300), (250, 375))
        if self.wrong_guesses >= 6:
            # Right leg
            draw_smooth_line((300, 300), (350, 375))
            
    def draw_word(self):
        word_display = ""
        spacing = 30  # Space between letters
        start_x = 400
        
        for i, letter in enumerate(self.word):
            if letter in self.guessed_letters:
                # Animate letter appearance
                if letter not in self.letter_animations:
                    self.letter_animations[letter] = (0, 0)  # (scale, alpha)
                
                scale, alpha = self.letter_animations[letter]
                if scale < 1.0:
                    scale = min(1.0, scale + 0.1)
                if alpha < 255:
                    alpha = min(255, alpha + 25)
                self.letter_animations[letter] = (scale, alpha)
                
                # Draw letter with animation
                letter_surf = self.font.render(letter, True, self.WHITE)
                letter_surf.set_alpha(alpha)
                scaled_size = (int(letter_surf.get_width() * scale), 
                             int(letter_surf.get_height() * scale))
                if scaled_size[0] > 0 and scaled_size[1] > 0:
                    letter_surf = pygame.transform.scale(letter_surf, scaled_size)
                pos_x = start_x + i * spacing - letter_surf.get_width()//2
                pos_y = 300 - letter_surf.get_height()//2
                self.screen.blit(letter_surf, (pos_x, pos_y))
            else:
                # Draw underscore
                pygame.draw.line(self.screen, self.GRAY,
                               (start_x + i * spacing - 10, 320),
                               (start_x + i * spacing + 10, 320), 2)
        
    def draw_guessed_letters(self):
        guessed = sorted(self.guessed_letters)
        x, y = 400, 400
        spacing = 30
        
        for i, letter in enumerate(guessed):
            color = self.RED if letter not in self.word else self.GREEN
            text = self.small_font.render(letter, True, color)
            self.screen.blit(text, (x + i * spacing, y))
            
    def draw_hint(self):
        if self.hint_showing:
            if self.hint_alpha < 255:
                self.hint_alpha = min(255, self.hint_alpha + 10)
                
            hint_text = self.small_font.render(f"Hint: {self.hint}", True, self.BLUE)
            hint_text.set_alpha(self.hint_alpha)
            self.screen.blit(hint_text, (50, 450))
        
    def draw_category(self):
        category = f"Category: {self.category_list[self.selected_category]}"
        text = self.small_font.render(category, True, self.BLUE)
        self.screen.blit(text, (400, 200))
        
    def draw_menu(self):
        self.screen.fill(self.BLACK)
        
        # Fade in animation
        if self.menu_alpha < 255:
            self.menu_alpha = min(255, self.menu_alpha + self.fade_speed)
        
        # Title with shadow
        shadow_offset = 2
        title = self.font.render("Select Category", True, self.GRAY)
        title_main = self.font.render("Select Category", True, self.WHITE)
        title_pos = (self.WIDTH//2 - title.get_width()//2, 100)
        title.set_alpha(self.menu_alpha)
        title_main.set_alpha(self.menu_alpha)
        self.screen.blit(title, (title_pos[0] + shadow_offset, title_pos[1] + shadow_offset))
        self.screen.blit(title_main, title_pos)
        
        # Category options with hover effect
        start_y = 250
        spacing = 60
        mouse_pos = pygame.mouse.get_pos()
        
        for i, category in enumerate(self.category_list):
            text_pos = (self.WIDTH//2, start_y + i * spacing)
            hover = abs(mouse_pos[1] - text_pos[1]) < 20
            
            color = self.WHITE if i == self.selected_category else \
                   self.LIGHT_GRAY if hover else self.GRAY
            text = self.small_font.render(category, True, color)
            text.set_alpha(self.menu_alpha)
            self.screen.blit(text, (text_pos[0] - text.get_width()//2, text_pos[1]))
        
        # Instructions
        instructions = self.small_font.render("Press ENTER to start", True, self.GRAY)
        instructions.set_alpha(self.menu_alpha)
        self.screen.blit(instructions, (self.WIDTH//2 - instructions.get_width()//2, self.HEIGHT - 100))
        
        # Quit instruction
        quit_text = self.small_font.render("Press Q to quit", True, self.GRAY)
        quit_text.set_alpha(self.menu_alpha)
        self.screen.blit(quit_text, (self.WIDTH - quit_text.get_width() - 20, 20))
        
        pygame.display.flip()
        
    def draw_game(self):
        self.screen.fill(self.BLACK)
        
        self.draw_hangman()
        self.draw_word()
        self.draw_guessed_letters()
        self.draw_category()
        self.draw_hint()
        
        # Draw menu and hint options
        menu_text = self.small_font.render("ESC - Menu", True, self.GRAY)
        hint_text = self.small_font.render("Ctrl+H - Show Hint", True, self.GRAY)
        self.screen.blit(menu_text, (20, 20))
        self.screen.blit(hint_text, (20, 60))
        
        if self.game_over:
            # Create semi-transparent overlay
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.fill(self.BLACK)
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            
            # Create message box
            box_width = 500
            box_height = 200
            box_x = self.WIDTH//2 - box_width//2
            box_y = self.HEIGHT//2 - box_height//2
            
            # Draw box background and border
            pygame.draw.rect(self.screen, self.GRAY, 
                           (box_x, box_y, box_width, box_height))
            pygame.draw.rect(self.screen, self.WHITE, 
                           (box_x, box_y, box_width, box_height), 3)
            
            # Draw message
            if self.won:
                text = self.font.render("You Won!", True, self.GREEN)
            else:
                text = self.font.render(f"Game Over! Word: {self.word}", True, self.RED)
            self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, box_y + 50))
            
            # Draw instructions
            restart = self.small_font.render("SPACE - Play again    ESC - Menu", True, self.WHITE)
            self.screen.blit(restart, (self.WIDTH//2 - restart.get_width()//2, box_y + 120))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Handle Ctrl+Q for quitting anytime
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        running = False
                        continue
                        
                    if self.state == self.MENU:
                        if event.key == pygame.K_UP:
                            self.selected_category = (self.selected_category - 1) % len(self.category_list)
                        elif event.key == pygame.K_DOWN:
                            self.selected_category = (self.selected_category + 1) % len(self.category_list)
                        elif event.key == pygame.K_RETURN:
                            self.state = self.PLAYING
                            self.menu_alpha = 0  # Reset fade for next menu entry
                            self.reset_game()
                    else:  # Đang trong game
                        if not self.game_over:
                            if event.key == pygame.K_ESCAPE:
                                self.state = self.MENU
                            # Handle Ctrl+H for hint
                            elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                self.hint_showing = True
                            elif event.unicode.isalpha():
                                letter = event.unicode.upper()
                                if letter not in self.guessed_letters:
                                    self.guessed_letters.add(letter)
                                    if letter not in self.word:
                                        self.wrong_guesses += 1
                                        if self.wrong_guesses >= self.max_wrong_guesses:
                                            self.game_over = True
                                    elif self.is_word_guessed():
                                        self.game_over = True
                                        self.won = True
                        else:  # Game over
                            if event.key == pygame.K_SPACE:
                                self.reset_game()
                            elif event.key == pygame.K_ESCAPE:
                                self.state = self.MENU
                                
            if self.state == self.MENU:
                self.draw_menu()
            else:
                self.draw_game()
            
            self.clock.tick(60)
        
        pygame.quit()

def main():
    game = HangmanGame()
    game.run()

if __name__ == "__main__":
    main() 