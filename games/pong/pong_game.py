import pygame
import random
import math

class PongGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Game states
        self.MENU = 0
        self.PLAYING = 1
        self.GAME_OVER = 2  # Add game over state
        self.state = self.MENU
        
        # Score limit
        self.SCORE_LIMIT = 10
        
        # Difficulty settings
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.selected_difficulty = 0
        self.ai_settings = {
            "Easy": {"speed": 5, "reaction_time": 30, "mistake_chance": 0.2},
            "Medium": {"speed": 7, "reaction_time": 20, "mistake_chance": 0.1},
            "Hard": {"speed": 10, "reaction_time": 10, "mistake_chance": 0.05}
        }
        
        self.reset_game()
        
    def reset_game(self):
        # Paddle settings
        self.PADDLE_WIDTH = 10
        self.PADDLE_HEIGHT = 100
        self.PADDLE_SPEED = 8
        self.player_y = self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2
        self.ai_y = self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2
        self.ai_target_y = self.ai_y
        self.ai_reaction_counter = 0
        
        # Ball settings
        self.BALL_SIZE = 10
        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        self.ball_speed = 7
        angle = random.uniform(-math.pi/4, math.pi/4)
        if random.random() < 0.5:
            angle += math.pi
        self.ball_dx = math.cos(angle) * self.ball_speed
        self.ball_dy = math.sin(angle) * self.ball_speed
        
        # Score
        self.player_score = 0
        self.ai_score = 0
        
    def handle_paddle_collision(self, paddle_y, is_player):
        # Calculate collision point relative to paddle center
        relative_intersect_y = (paddle_y + self.PADDLE_HEIGHT/2) - self.ball_y
        normalized_intersect = relative_intersect_y / (self.PADDLE_HEIGHT/2)
        bounce_angle = normalized_intersect * math.pi/3  # Max 60 degree bounce
        
        speed = math.sqrt(self.ball_dx * self.ball_dx + self.ball_dy * self.ball_dy)
        if is_player:
            self.ball_dx = abs(speed * math.cos(bounce_angle))
        else:
            self.ball_dx = -abs(speed * math.cos(bounce_angle))
        self.ball_dy = -speed * math.sin(bounce_angle)
        
        # Move ball slightly away from paddle to prevent sticking
        if is_player:
            self.ball_x = self.PADDLE_WIDTH + self.BALL_SIZE
        else:
            self.ball_x = self.WIDTH - self.PADDLE_WIDTH - self.BALL_SIZE
        
    def update_ai(self):
        difficulty = self.ai_settings[self.difficulties[self.selected_difficulty]]
        
        # Update AI target with reaction delay
        self.ai_reaction_counter += 1
        if self.ai_reaction_counter >= difficulty["reaction_time"]:
            self.ai_reaction_counter = 0
            
            # Occasionally make mistakes
            if random.random() < difficulty["mistake_chance"]:
                self.ai_target_y = random.randint(0, self.HEIGHT - self.PADDLE_HEIGHT)
            else:
                self.ai_target_y = self.ball_y - self.PADDLE_HEIGHT/2
        
        # Move AI paddle towards target
        if abs(self.ai_target_y - self.ai_y) > difficulty["speed"]:
            if self.ai_target_y > self.ai_y:
                self.ai_y += difficulty["speed"]
            else:
                self.ai_y -= difficulty["speed"]
        
        # Keep AI paddle within screen bounds
        self.ai_y = max(0, min(self.HEIGHT - self.PADDLE_HEIGHT, self.ai_y))
        
    def update_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Ball collision with top and bottom
        if self.ball_y <= 0 or self.ball_y >= self.HEIGHT - self.BALL_SIZE:
            self.ball_dy = -self.ball_dy
            self.ball_y = max(0, min(self.HEIGHT - self.BALL_SIZE, self.ball_y))
        
        # Ball collision with paddles
        if (self.ball_dx < 0 and 
            self.ball_x <= self.PADDLE_WIDTH and 
            self.player_y <= self.ball_y <= self.player_y + self.PADDLE_HEIGHT):
            self.handle_paddle_collision(self.player_y, True)
            
        elif (self.ball_dx > 0 and 
              self.ball_x >= self.WIDTH - self.PADDLE_WIDTH - self.BALL_SIZE and 
              self.ai_y <= self.ball_y <= self.ai_y + self.PADDLE_HEIGHT):
            self.handle_paddle_collision(self.ai_y, False)
        
        # Ball out of bounds
        if self.ball_x < 0:
            self.ai_score += 1
            self.reset_ball()
        elif self.ball_x > self.WIDTH:
            self.player_score += 1
            self.reset_ball()
            
    def reset_ball(self):
        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        angle = random.uniform(-math.pi/4, math.pi/4)
        if random.random() < 0.5:
            angle += math.pi
        self.ball_speed = 7
        self.ball_dx = math.cos(angle) * self.ball_speed
        self.ball_dy = math.sin(angle) * self.ball_speed
        
    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        
        # Title
        title = self.font.render("Select Difficulty", True, (255, 255, 255))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 100))
        
        # Difficulty options
        start_y = 250
        spacing = 60
        for i, diff in enumerate(self.difficulties):
            color = (255, 255, 255) if i == self.selected_difficulty else (128, 128, 128)
            text = self.small_font.render(diff, True, color)
            self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, start_y + i * spacing))
        
        # Instructions
        instructions = self.small_font.render("Press ENTER to start", True, (128, 128, 128))
        self.screen.blit(instructions, (self.WIDTH//2 - instructions.get_width()//2, self.HEIGHT - 100))
        
        # Thêm nút thoát
        quit_text = self.small_font.render("ESC - Back to Menu", True, (128, 128, 128))
        self.screen.blit(quit_text, (20, 20))
        
        pygame.display.flip()
        
    def draw_game(self):
        self.screen.fill((0, 0, 0))
        
        # Draw paddles
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (0, self.player_y, self.PADDLE_WIDTH, self.PADDLE_HEIGHT))
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (self.WIDTH - self.PADDLE_WIDTH, self.ai_y,
                         self.PADDLE_WIDTH, self.PADDLE_HEIGHT))
        
        # Draw ball
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (self.ball_x, self.ball_y, self.BALL_SIZE, self.BALL_SIZE))
        
        # Draw scores and player indicators
        player_text = self.font.render(str(self.player_score), True, (255, 255, 255))
        ai_text = self.font.render(str(self.ai_score), True, (255, 255, 255))
        
        # Draw player labels
        player_label = self.small_font.render("PLAYER", True, (128, 128, 128))
        ai_label = self.small_font.render("AI", True, (128, 128, 128))
        
        # Position scores and labels
        self.screen.blit(player_text, (self.WIDTH//4, 50))
        self.screen.blit(ai_text, (3*self.WIDTH//4, 50))
        self.screen.blit(player_label, (self.WIDTH//4 - player_label.get_width()//2, 20))
        self.screen.blit(ai_label, (3*self.WIDTH//4 - ai_label.get_width()//2, 20))
        
        # Draw difficulty level
        diff_text = self.small_font.render(f"Difficulty: {self.difficulties[self.selected_difficulty]}", 
                                         True, (128, 128, 128))
        self.screen.blit(diff_text, (self.WIDTH//2 - diff_text.get_width()//2, 20))
        
        # Draw controls hint
        controls = self.small_font.render("W/S - Move    ESC - Menu", True, (128, 128, 128))
        self.screen.blit(controls, (self.WIDTH//2 - controls.get_width()//2, self.HEIGHT - 40))
        
        # Draw game over screen if someone won
        if self.state == self.GAME_OVER:
            # Create semi-transparent overlay
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            
            # Create message box
            box_width = 400
            box_height = 160
            box_x = self.WIDTH//2 - box_width//2
            box_y = self.HEIGHT//2 - box_height//2
            
            # Draw box background and border
            pygame.draw.rect(self.screen, (128, 128, 128), 
                           (box_x, box_y, box_width, box_height))
            pygame.draw.rect(self.screen, (255, 255, 255), 
                           (box_x, box_y, box_width, box_height), 3)
            
            # Draw winner message
            winner = "You Won!" if self.player_score >= self.SCORE_LIMIT else "AI Won!"
            color = (0, 255, 0) if self.player_score >= self.SCORE_LIMIT else (255, 0, 0)
            text = self.font.render(winner, True, color)
            score_text = self.small_font.render(f"Final Score: {self.player_score} - {self.ai_score}", 
                                              True, (255, 255, 255))
            restart = self.small_font.render("SPACE - Play again    ESC - Menu", 
                                           True, (255, 255, 255))
            
            self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, box_y + 30))
            self.screen.blit(score_text, (self.WIDTH//2 - score_text.get_width()//2, box_y + 80))
            self.screen.blit(restart, (self.WIDTH//2 - restart.get_width()//2, box_y + 120))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == self.MENU:
                        if event.key == pygame.K_UP:
                            self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
                        elif event.key == pygame.K_DOWN:
                            self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
                        elif event.key == pygame.K_RETURN:
                            self.state = self.PLAYING
                        elif event.key == pygame.K_ESCAPE:
                            return  # Return to main menu
                    elif event.key == pygame.K_ESCAPE:
                        self.state = self.MENU
                        self.reset_game()
            
            if self.state == self.MENU:
                self.draw_menu()
            elif self.state == self.PLAYING:
                # Handle player input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and self.player_y > 0:
                    self.player_y -= self.PADDLE_SPEED
                if keys[pygame.K_s] and self.player_y < self.HEIGHT - self.PADDLE_HEIGHT:
                    self.player_y += self.PADDLE_SPEED
                
                # Update game state
                self.update_ai()
                self.update_ball()
                
                # Check for winner
                if self.player_score >= self.SCORE_LIMIT or self.ai_score >= self.SCORE_LIMIT:
                    self.state = self.GAME_OVER
                
                self.draw_game()
            else:  # GAME_OVER state
                self.draw_game()
            
            self.clock.tick(60)
        
        return

def main():
    # Only initialize the game without running
    return PongGame()

if __name__ == "__main__":
    # When running this file directly, show message
    print("Please run the game from the main menu (main.py)") 