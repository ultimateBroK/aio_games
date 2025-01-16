import pygame
import sys
import random
import os

class TetrisGame:
    # Constants
    BLOCK_SIZE = 30
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    SIDEBAR_WIDTH = 200
    WIDTH = GRID_WIDTH * BLOCK_SIZE + SIDEBAR_WIDTH
    HEIGHT = GRID_HEIGHT * BLOCK_SIZE
    FPS = 60

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    FLASH_WHITE = (220, 220, 220)
    COLORS = [
        (0, 255, 255),  # I piece - Cyan
        (0, 0, 255),    # J piece - Blue
        (255, 128, 0),  # L piece - Orange
        (255, 255, 0),  # O piece - Yellow
        (0, 255, 0),    # S piece - Green
        (128, 0, 128),  # T piece - Purple
        (255, 0, 0),    # Z piece - Red
    ]

    # Tetromino shapes
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 0, 0],      # J
         [1, 1, 1]],
        [[0, 0, 1],      # L
         [1, 1, 1]],
        [[1, 1],         # O
         [1, 1]],
        [[0, 1, 1],      # S
         [1, 1, 0]],
        [[0, 1, 0],      # T
         [1, 1, 1]],
        [[1, 1, 0],      # Z
         [0, 1, 1]]
    ]

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tetris")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        
        # Load sounds
        sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        self.move_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'move.wav'))
        self.rotate_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'rotate.wav'))
        self.drop_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'drop.wav'))
        self.clear_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'clear.wav'))
        self.gameover_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'gameover.wav'))
        
        self.reset_game()
        self.running = True
        self.fall_time = 0
        self.fall_speed = 500
        self.last_fall = pygame.time.get_ticks()
        self.clearing_lines = False
        self.clear_animation_start = 0
        self.lines_to_clear = []

    def is_valid_move(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if (not 0 <= x + j < self.GRID_WIDTH or
                        not 0 <= y + i < self.GRID_HEIGHT or
                        self.grid[y + i][x + j]):
                        return False
        return True

    def reset_game(self):
        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.clearing_lines = False
        self.lines_to_clear = []
        self.new_piece()
        self.generate_next_piece()

    def generate_next_piece(self):
        shape_idx = random.randint(0, len(self.SHAPES) - 1)
        self.next_piece = {
            'shape': self.SHAPES[shape_idx],
            'color': self.COLORS[shape_idx]
        }

    def new_piece(self):
        if hasattr(self, 'next_piece'):
            self.current_piece = {
                'shape': self.next_piece['shape'],
                'color': self.next_piece['color'],
                'x': self.GRID_WIDTH // 2 - len(self.next_piece['shape'][0]) // 2,
                'y': 0
            }
        else:
            shape_idx = random.randint(0, len(self.SHAPES) - 1)
            self.current_piece = {
                'shape': self.SHAPES[shape_idx],
                'color': self.COLORS[shape_idx],
                'x': self.GRID_WIDTH // 2 - len(self.SHAPES[shape_idx][0]) // 2,
                'y': 0
            }
        
        self.generate_next_piece()
        
        if not self.is_valid_move(self.current_piece['shape'], 
                                self.current_piece['x'], 
                                self.current_piece['y']):
            self.game_over = True
            pygame.mixer.Sound.play(self.gameover_sound)

    def check_lines(self):
        self.lines_to_clear = []
        for i in range(self.GRID_HEIGHT):
            if all(self.grid[i]):
                self.lines_to_clear.append(i)
        
        if self.lines_to_clear:
            self.clearing_lines = True
            self.clear_animation_start = pygame.time.get_ticks()
            pygame.mixer.Sound.play(self.clear_sound)

    def clear_lines(self):
        for line in self.lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(self.GRID_WIDTH)])
        
        # Update score and level
        lines_cleared = len(self.lines_to_clear)
        self.lines += lines_cleared
        self.score += lines_cleared * 100 * self.level
        self.level = self.lines // 10 + 1
        self.fall_speed = max(100, 500 - (self.level - 1) * 50)
        
        self.clearing_lines = False
        self.lines_to_clear = []

    def place_piece(self):
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']
        
        pygame.mixer.Sound.play(self.drop_sound)
        self.check_lines()
        if not self.clearing_lines:
            self.new_piece()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Back to menu
                    self.running = False
                    return True
                if not self.game_over and not self.clearing_lines:
                    if event.key == pygame.K_LEFT:
                        if self.is_valid_move(self.current_piece['shape'],
                                           self.current_piece['x'] - 1,
                                           self.current_piece['y']):
                            self.current_piece['x'] -= 1
                            pygame.mixer.Sound.play(self.move_sound)
                    elif event.key == pygame.K_RIGHT:
                        if self.is_valid_move(self.current_piece['shape'],
                                           self.current_piece['x'] + 1,
                                           self.current_piece['y']):
                            self.current_piece['x'] += 1
                            pygame.mixer.Sound.play(self.move_sound)
                    elif event.key == pygame.K_DOWN:
                        if self.is_valid_move(self.current_piece['shape'],
                                           self.current_piece['x'],
                                           self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                            pygame.mixer.Sound.play(self.move_sound)
                    elif event.key == pygame.K_UP:
                        rotated = list(zip(*self.current_piece['shape'][::-1]))
                        if self.is_valid_move(rotated,
                                           self.current_piece['x'],
                                           self.current_piece['y']):
                            self.current_piece['shape'] = rotated
                            pygame.mixer.Sound.play(self.rotate_sound)
                elif event.key == pygame.K_SPACE:
                    self.reset_game()
        return True

    def update(self):
        if self.game_over or self.clearing_lines:
            if self.clearing_lines:
                current_time = pygame.time.get_ticks()
                if current_time - self.clear_animation_start > 200:  # Animation duration
                    self.clear_lines()
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall > self.fall_speed:
            if self.is_valid_move(self.current_piece['shape'],
                               self.current_piece['x'],
                               self.current_piece['y'] + 1):
                self.current_piece['y'] += 1
            else:
                self.place_piece()
            self.last_fall = current_time

    def draw(self):
        self.screen.fill(self.BLACK)
        self.draw_grid_lines()
        
        # Draw grid
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color:
                    # Flash effect for lines being cleared
                    if self.clearing_lines and y in self.lines_to_clear:
                        if (pygame.time.get_ticks() // 100) % 2:  # Flash every 100ms
                            color = self.FLASH_WHITE
                    pygame.draw.rect(self.screen, color,
                                   (x * self.BLOCK_SIZE,
                                    y * self.BLOCK_SIZE,
                                    self.BLOCK_SIZE - 1,
                                    self.BLOCK_SIZE - 1))

        # Draw current piece
        if not self.game_over and not self.clearing_lines:
            for i, row in enumerate(self.current_piece['shape']):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen,
                                       self.current_piece['color'],
                                       ((self.current_piece['x'] + j) * self.BLOCK_SIZE,
                                        (self.current_piece['y'] + i) * self.BLOCK_SIZE,
                                        self.BLOCK_SIZE - 1,
                                        self.BLOCK_SIZE - 1))

        # Draw stats and next piece
        self.draw_stats()
        self.draw_next_piece()

        # Draw game over
        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, self.WHITE)
            replay_text = self.small_font.render("Press SPACE to play again", True, self.WHITE)
            self.screen.blit(game_over_text, 
                           (self.GRID_WIDTH * self.BLOCK_SIZE + 10, 
                            self.HEIGHT // 2 + 100))
            self.screen.blit(replay_text,
                           (self.GRID_WIDTH * self.BLOCK_SIZE + 10,
                            self.HEIGHT // 2 + 150))

        # Draw back button
        back_text = self.small_font.render("Press ESC for menu", True, self.WHITE)
        self.screen.blit(back_text, (10, 10))

        pygame.display.flip()

    def draw_grid_lines(self):
        # Vẽ đường kẻ dọc
        for x in range(self.GRID_WIDTH + 1):
            pygame.draw.line(self.screen, self.GRAY,
                           (x * self.BLOCK_SIZE, 0),
                           (x * self.BLOCK_SIZE, self.HEIGHT))
        
        # Vẽ đường kẻ ngang
        for y in range(self.GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, self.GRAY,
                           (0, y * self.BLOCK_SIZE),
                           (self.GRID_WIDTH * self.BLOCK_SIZE, y * self.BLOCK_SIZE))

    def draw_next_piece(self):
        next_piece_text = self.font.render("Next:", True, self.WHITE)
        self.screen.blit(next_piece_text, 
                        (self.GRID_WIDTH * self.BLOCK_SIZE + 20, 100))

        start_x = self.GRID_WIDTH * self.BLOCK_SIZE + 50
        start_y = 150
        
        for i, row in enumerate(self.next_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen,
                                   self.next_piece['color'],
                                   (start_x + j * self.BLOCK_SIZE,
                                    start_y + i * self.BLOCK_SIZE,
                                    self.BLOCK_SIZE - 1,
                                    self.BLOCK_SIZE - 1))

    def draw_stats(self):
        # Vẽ khung thông tin bên phải
        sidebar_rect = pygame.Rect(self.GRID_WIDTH * self.BLOCK_SIZE, 0,
                                 self.SIDEBAR_WIDTH, self.HEIGHT)
        pygame.draw.rect(self.screen, self.DARK_GRAY, sidebar_rect)
        
        # Vẽ điểm số
        score_text = self.font.render(f"Score:", True, self.WHITE)
        score_value = self.font.render(str(self.score), True, self.WHITE)
        self.screen.blit(score_text, (self.GRID_WIDTH * self.BLOCK_SIZE + 20, 10))
        self.screen.blit(score_value, (self.GRID_WIDTH * self.BLOCK_SIZE + 20, 40))

        # Vẽ số dòng đã xóa
        lines_text = self.font.render(f"Lines:", True, self.WHITE)
        lines_value = self.font.render(str(self.lines), True, self.WHITE)
        self.screen.blit(lines_text, (self.GRID_WIDTH * self.BLOCK_SIZE + 20, 250))
        self.screen.blit(lines_value, (self.GRID_WIDTH * self.BLOCK_SIZE + 20, 280))

        # Vẽ level
        level_text = self.font.render(f"Level:", True, self.WHITE)
        level_value = self.font.render(str(self.level), True, self.WHITE)
        self.screen.blit(level_text, (self.GRID_WIDTH * self.BLOCK_SIZE + 20, 350))
        self.screen.blit(level_value, (self.GRID_WIDTH * self.BLOCK_SIZE + 20, 380))

    def run(self):
        self.running = True
        while self.running:
            if not self.handle_events():
                pygame.quit()
                sys.exit()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

def main():
    game = TetrisGame()
    game.run()

if __name__ == "__main__":
    main() 