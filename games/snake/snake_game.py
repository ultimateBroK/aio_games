import pygame
import sys
import random

class SnakeGame:
    # Constants
    WIDTH, HEIGHT = 800, 600
    BLOCK_SIZE = 20
    FPS = 10
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.running = True

    class Snake:
        def __init__(self, game):
            self.game = game
            self.body = [(200, 200), (220, 200), (240, 200)]
            self.direction = 'RIGHT'
            self.alive = True

        def move(self):
            head = self.body[-1]
            moves = {
                'RIGHT': (head[0] + self.game.BLOCK_SIZE, head[1]),
                'LEFT': (head[0] - self.game.BLOCK_SIZE, head[1]),
                'UP': (head[0], head[1] - self.game.BLOCK_SIZE),
                'DOWN': (head[0], head[1] + self.game.BLOCK_SIZE)
            }
            self.body.append(moves[self.direction])
            self.body.pop(0)

        def turn(self, new_dir):
            opposites = {'RIGHT': 'LEFT', 'LEFT': 'RIGHT', 'UP': 'DOWN', 'DOWN': 'UP'}
            if opposites[self.direction] != new_dir:
                self.direction = new_dir

    class Apple:
        def __init__(self, game):
            self.game = game
            self.new_position()

        def new_position(self):
            self.position = (
                random.randint(0, (self.game.WIDTH - self.game.BLOCK_SIZE) // self.game.BLOCK_SIZE) * self.game.BLOCK_SIZE,
                random.randint(0, (self.game.HEIGHT - self.game.BLOCK_SIZE) // self.game.BLOCK_SIZE) * self.game.BLOCK_SIZE
            )

    def reset_game(self):
        self.snake = self.Snake(self)
        self.apple = self.Apple(self)
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Back to menu
                    self.running = False
                    return True
                if event.key == pygame.K_SPACE and not self.snake.alive:
                    self.reset_game()
                for key, direction in [(pygame.K_UP, 'UP'), (pygame.K_DOWN, 'DOWN'),
                                     (pygame.K_LEFT, 'LEFT'), (pygame.K_RIGHT, 'RIGHT')]:
                    if event.key == key and self.snake.alive:
                        self.snake.turn(direction)
        return True

    def update(self):
        if not self.snake.alive:
            return

        self.snake.move()
        head = self.snake.body[-1]

        # Check collisions
        if (head[0] < 0 or head[0] >= self.WIDTH or head[1] < 0 or head[1] >= self.HEIGHT 
            or head in self.snake.body[:-1]):
            self.snake.alive = False
            return

        if head == self.apple.position:
            self.snake.body.insert(0, self.snake.body[0])
            self.apple.new_position()
            self.score += 1

    def draw(self):
        self.screen.fill(self.BLACK)

        if not self.snake.alive:
            text = self.font.render("Game Over!", True, self.WHITE)
            replay_text = self.font.render("Press SPACE to play again", True, self.WHITE)
            self.screen.blit(text, (self.WIDTH // 2 - 75, self.HEIGHT // 2 - 50))
            self.screen.blit(replay_text, (self.WIDTH // 2 - 150, self.HEIGHT // 2 + 50))
        else:
            # Draw snake
            for pos in self.snake.body:
                pygame.draw.rect(self.screen, self.GREEN, (*pos, self.BLOCK_SIZE, self.BLOCK_SIZE))
            
            # Draw apple
            pygame.draw.rect(self.screen, self.RED, (*self.apple.position, self.BLOCK_SIZE, self.BLOCK_SIZE))

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (self.WIDTH - 120, 10))

        # Draw back button
        back_text = self.small_font.render("Press ESC for menu", True, self.WHITE)
        self.screen.blit(back_text, (10, 10))

        pygame.display.flip()

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
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main() 