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
    GRAY = (128, 128, 128)
    PADDLE_WIDTH = 15
    PADDLE_HEIGHT = 90
    BALL_SIZE = 15
    PADDLE_SPEED = 5
    BALL_SPEED = 7
    
    # AI Difficulty Settings
    AI_SETTINGS = {
        'easy': {'speed': 3.5, 'delay': 10, 'mistake_chance': 0.3},
        'medium': {'speed': 4.5, 'delay': 5, 'mistake_chance': 0.1},
        'hard': {'speed': 5.5, 'delay': 2, 'mistake_chance': 0.0}
    }

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong vs AI")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.difficulty = 'medium'  # Mặc định là medium
        self.ball_history = []  # Initialize ball_history before reset_game
        self.choosing_difficulty = False
        self.running = True
        self.reset_game()

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
        self._reset_ball()
        # Scores
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.ball_history = []

    def update_ai(self):
        settings = self.AI_SETTINGS[self.difficulty]
        
        # Lấy vị trí bóng với delay
        self.ball_history.append(self.ball.centery)
        if len(self.ball_history) > settings['delay']:
            target_y = self.ball_history.pop(0)
        else:
            target_y = self.ball.centery

        # Thỉnh thoảng AI sẽ mắc lỗi (tùy theo độ khó)
        if random.random() < settings['mistake_chance']:
            target_y = random.randint(0, self.HEIGHT)

        # Di chuyển paddle AI
        if self.ball_speed_x > 0:  # Chỉ di chuyển khi bóng đang đi về phía AI
            if self.right_paddle.centery < target_y - self.PADDLE_HEIGHT//4:
                self.right_paddle.y += settings['speed']
            elif self.right_paddle.centery > target_y + self.PADDLE_HEIGHT//4:
                self.right_paddle.y -= settings['speed']

        # Giới hạn paddle trong màn hình
        if self.right_paddle.top < 0:
            self.right_paddle.top = 0
        if self.right_paddle.bottom > self.HEIGHT:
            self.right_paddle.bottom = self.HEIGHT

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Back to menu
                    self.running = False
                    return True
                if self.choosing_difficulty:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        self.difficulty = {
                            pygame.K_1: 'easy',
                            pygame.K_2: 'medium',
                            pygame.K_3: 'hard'
                        }[event.key]
                        self.choosing_difficulty = False
                        self.reset_game()
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.choosing_difficulty = True
                    elif not self.game_over and self.choosing_difficulty:
                        self.choosing_difficulty = False
                        self.reset_game()
        return True

    def update(self):
        if self.game_over or self.choosing_difficulty:
            return

        # Player paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.left_paddle.top > 0:
            self.left_paddle.y -= self.PADDLE_SPEED
        if keys[pygame.K_s] and self.left_paddle.bottom < self.HEIGHT:
            self.left_paddle.y += self.PADDLE_SPEED

        # Update AI
        self.update_ai()

        # Ball movement
        next_x = self.ball.x + self.ball_speed_x
        next_y = self.ball.y + self.ball_speed_y
        
        # Kiểm tra va chạm trước khi di chuyển
        next_ball = pygame.Rect(next_x, next_y, self.BALL_SIZE, self.BALL_SIZE)
        
        # Ball collision with paddles
        paddle_hit = False
        if next_ball.colliderect(self.left_paddle) or next_ball.colliderect(self.right_paddle):
            self.ball_speed_x *= -1
            # Thêm góc nảy dựa trên vị trí chạm paddle
            if next_ball.colliderect(self.left_paddle):
                relative_intersect_y = (self.left_paddle.centery - next_ball.centery)
            else:
                relative_intersect_y = (self.right_paddle.centery - next_ball.centery)
            normalized_intersect = relative_intersect_y / (self.PADDLE_HEIGHT / 2)
            bounce_angle = normalized_intersect * 0.75  # Giới hạn góc nảy
            self.ball_speed_y = -self.BALL_SPEED * bounce_angle
            paddle_hit = True

        # Ball collision with top and bottom
        if next_ball.top <= 0 or next_ball.bottom >= self.HEIGHT:
            self.ball_speed_y *= -1

        # Di chuyển bóng nếu không có va chạm với paddle
        if not paddle_hit:
            self.ball.x = next_x
            self.ball.y = next_y

        # Scoring
        if self.ball.left <= 0:
            self.ai_score += 1
            if self.ai_score >= 5:
                self.game_over = True
            else:
                self._reset_ball()
        elif self.ball.right >= self.WIDTH:
            self.player_score += 1
            if self.player_score >= 5:
                self.game_over = True
            else:
                self._reset_ball()

    def _reset_ball(self):
        self.ball.center = (self.WIDTH//2, self.HEIGHT//2)
        # Đảm bảo bóng không đi quá thẳng
        angle = random.uniform(-0.5, 0.5)  # Góc giới hạn khoảng -30 đến 30 độ
        self.ball_speed_x = self.BALL_SPEED * random.choice((1, -1))
        self.ball_speed_y = self.BALL_SPEED * angle
        self.ball_history.clear()

    def draw(self):
        self.screen.fill(self.BLACK)
        
        if self.choosing_difficulty:
            # Vẽ menu chọn độ khó
            title = self.font.render("Choose Difficulty:", True, self.WHITE)
            easy = self.font.render("1. Easy", True, self.WHITE)
            medium = self.font.render("2. Medium", True, self.WHITE)
            hard = self.font.render("3. Hard", True, self.WHITE)
            
            self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 200))
            self.screen.blit(easy, (self.WIDTH//2 - easy.get_width()//2, 300))
            self.screen.blit(medium, (self.WIDTH//2 - medium.get_width()//2, 350))
            self.screen.blit(hard, (self.WIDTH//2 - hard.get_width()//2, 400))
        else:
            # Draw paddles and ball
            pygame.draw.rect(self.screen, self.WHITE, self.left_paddle)
            pygame.draw.rect(self.screen, self.WHITE, self.right_paddle)
            pygame.draw.ellipse(self.screen, self.WHITE, self.ball)
            
            # Draw center line
            pygame.draw.aaline(self.screen, self.GRAY, 
                             (self.WIDTH//2, 0), (self.WIDTH//2, self.HEIGHT))

            # Draw scores
            player_text = self.font.render(str(self.player_score), True, self.WHITE)
            ai_text = self.font.render(str(self.ai_score), True, self.WHITE)
            self.screen.blit(player_text, (self.WIDTH//4, 20))
            self.screen.blit(ai_text, (3*self.WIDTH//4, 20))

            # Draw difficulty
            diff_text = self.small_font.render(f"Difficulty: {self.difficulty.title()}", True, self.GRAY)
            self.screen.blit(diff_text, (self.WIDTH//2 - diff_text.get_width()//2, 20))

            if self.game_over:
                winner = "You win!" if self.player_score >= 5 else "AI wins!"
                game_over_text = self.font.render(winner, True, self.WHITE)
                replay_text = self.small_font.render("Press SPACE to change difficulty", True, self.WHITE)
                self.screen.blit(game_over_text, (self.WIDTH//2 - game_over_text.get_width()//2, self.HEIGHT//2))
                self.screen.blit(replay_text, (self.WIDTH//2 - replay_text.get_width()//2, self.HEIGHT//2 + 50))

            # Draw controls
            controls_text = self.small_font.render("W/S to move", True, self.WHITE)
            self.screen.blit(controls_text, (10, self.HEIGHT - 30))

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