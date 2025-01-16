import pygame
import sys
import random

class PongGame:
    # Constants
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PADDLE_WIDTH = 15
    PADDLE_HEIGHT = 90
    BALL_SIZE = 15
    PADDLE_SPEED = 5
    BALL_SPEED = 7

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.running = True

    def reset_game(self):
        # Paddles
        self.left_paddle = pygame.Rect(50, self.HEIGHT//2 - self.PADDLE_HEIGHT//2,
                                     self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.right_paddle = pygame.Rect(self.WIDTH - 50 - self.PADDLE_WIDTH,
                                      self.HEIGHT//2 - self.PADDLE_HEIGHT//2,
                                      self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        # Ball
        self.ball = pygame.Rect(self.WIDTH//2 - self.BALL_SIZE//2,
                              self.HEIGHT//2 - self.BALL_SIZE//2,
                              self.BALL_SIZE, self.BALL_SIZE)
        self.ball_speed_x = self.BALL_SPEED * random.choice((1, -1))
        self.ball_speed_y = self.BALL_SPEED * random.choice((1, -1))
        # Scores
        self.left_score = 0
        self.right_score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Back to menu
                    self.running = False
                    return True
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        if self.game_over:
            return

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.left_paddle.top > 0:
            self.left_paddle.y -= self.PADDLE_SPEED
        if keys[pygame.K_s] and self.left_paddle.bottom < self.HEIGHT:
            self.left_paddle.y += self.PADDLE_SPEED
        if keys[pygame.K_UP] and self.right_paddle.top > 0:
            self.right_paddle.y -= self.PADDLE_SPEED
        if keys[pygame.K_DOWN] and self.right_paddle.bottom < self.HEIGHT:
            self.right_paddle.y += self.PADDLE_SPEED

        # Ball movement
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # Ball collision with top and bottom
        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.ball_speed_y *= -1

        # Ball collision with paddles
        if self.ball.colliderect(self.left_paddle) or self.ball.colliderect(self.right_paddle):
            self.ball_speed_x *= -1

        # Scoring
        if self.ball.left <= 0:
            self.right_score += 1
            if self.right_score >= 5:
                self.game_over = True
            else:
                self._reset_ball()
        elif self.ball.right >= self.WIDTH:
            self.left_score += 1
            if self.left_score >= 5:
                self.game_over = True
            else:
                self._reset_ball()

    def _reset_ball(self):
        self.ball.center = (self.WIDTH//2, self.HEIGHT//2)
        self.ball_speed_x = self.BALL_SPEED * random.choice((1, -1))
        self.ball_speed_y = self.BALL_SPEED * random.choice((1, -1))

    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Draw paddles and ball
        pygame.draw.rect(self.screen, self.WHITE, self.left_paddle)
        pygame.draw.rect(self.screen, self.WHITE, self.right_paddle)
        pygame.draw.ellipse(self.screen, self.WHITE, self.ball)
        
        # Draw center line
        pygame.draw.aaline(self.screen, self.WHITE, 
                         (self.WIDTH//2, 0), (self.WIDTH//2, self.HEIGHT))

        # Draw scores
        left_text = self.font.render(str(self.left_score), True, self.WHITE)
        right_text = self.font.render(str(self.right_score), True, self.WHITE)
        self.screen.blit(left_text, (self.WIDTH//4, 20))
        self.screen.blit(right_text, (3*self.WIDTH//4, 20))

        if self.game_over:
            winner = "Left Player" if self.left_score >= 5 else "Right Player"
            game_over_text = self.font.render(f"{winner} Wins!", True, self.WHITE)
            replay_text = self.small_font.render("Press SPACE to play again", True, self.WHITE)
            self.screen.blit(game_over_text, (self.WIDTH//2 - game_over_text.get_width()//2, self.HEIGHT//2))
            self.screen.blit(replay_text, (self.WIDTH//2 - replay_text.get_width()//2, self.HEIGHT//2 + 50))

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
    game = PongGame()
    game.run()

if __name__ == "__main__":
    main() 