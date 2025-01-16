import pygame
import random
import math

class Particle:
    def __init__(self, x, y, speed, angle, color, size, lifetime):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.age += 1
        return self.age < self.lifetime
        
    def draw(self, surface):
        alpha = 255 * (1 - self.age / self.lifetime)
        color = (*self.color, int(alpha))
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size, self.size), self.size)
        surface.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.colors = [(70, 130, 180), (100, 149, 237), (30, 144, 255)]  # Shades of blue
        
    def update(self):
        # Create new particles
        if len(self.particles) < 50 and random.random() < 0.1:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            speed = random.uniform(0.5, 2.0)
            angle = random.uniform(0, 2 * math.pi)
            color = random.choice(self.colors)
            size = random.randint(2, 5)
            lifetime = random.randint(60, 180)
            self.particles.append(Particle(x, y, speed, angle, color, size, lifetime))
        
        # Update existing particles
        self.particles = [p for p in self.particles if p.update()]
        
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

class Transition:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.progress = 0
        self.speed = 0.02
        self.fading_out = True
        
    def update(self):
        if self.fading_out:
            self.progress = min(1, self.progress + self.speed)
        else:
            self.progress = max(0, self.progress - self.speed)
            
    def is_done(self):
        return (self.fading_out and self.progress >= 1) or (not self.fading_out and self.progress <= 0)
        
    def draw(self, surface):
        alpha = int(255 * self.progress)
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        surface.blit(overlay, (0, 0))

class GamePreview:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.preview_size = (120, 120)
        self.preview_surface = pygame.Surface(self.preview_size)
        self.animation_counter = 0
        
        # Snake game variables
        self.snake_dir = (1, 0)
        self.snake_pos = [(3, 5), (4, 5), (5, 5)]
        self.food_pos = (7, 5)
        
        # Pong game variables
        self.ball_dx = 1
        self.ball_dy = 1
        self.ai_paddle_y = 35
        self.player_paddle_y = 35
        
        # Tetris variables
        self.current_piece = 0
        self.piece_y = 0
        self.fall_counter = 0
        
    def draw(self, screen, game_name, position):
        self.animation_counter = (self.animation_counter + 1) % 60
        self.preview_surface.fill((0, 0, 0))
        
        if game_name == "Snake Game":
            # Update snake position
            if self.animation_counter % 10 == 0:
                # Move snake
                new_head = (self.snake_pos[-1][0] + self.snake_dir[0],
                          self.snake_pos[-1][1] + self.snake_dir[1])
                
                # Check if snake reached food
                if new_head == self.food_pos:
                    self.snake_pos.append(new_head)
                    self.food_pos = ((self.food_pos[0] + 3) % 10,
                                   (self.food_pos[1] + 2) % 10)
                else:
                    self.snake_pos = self.snake_pos[1:] + [new_head]
                
                # Change direction occasionally
                if self.animation_counter % 30 == 0:
                    if self.snake_dir == (1, 0):
                        self.snake_dir = (0, 1)
                    elif self.snake_dir == (0, 1):
                        self.snake_dir = (-1, 0)
                    elif self.snake_dir == (-1, 0):
                        self.snake_dir = (0, -1)
                    else:
                        self.snake_dir = (1, 0)
            
            # Draw snake
            for segment in self.snake_pos:
                pygame.draw.rect(self.preview_surface, (0, 255, 0),
                               (segment[0] * 12, segment[1] * 12, 10, 10))
            
            # Draw food
            pygame.draw.rect(self.preview_surface, (255, 0, 0),
                           (self.food_pos[0] * 12, self.food_pos[1] * 12, 10, 10))
                           
        elif game_name == "Hangman":
            # Animate hangman drawing
            progress = (self.animation_counter // 10) % 7
            
            # Draw gallows
            pygame.draw.line(self.preview_surface, (255, 255, 255),
                           (30, 100), (90, 100), 2)  # Base
            if progress >= 1:
                pygame.draw.line(self.preview_surface, (255, 255, 255),
                               (60, 100), (60, 20), 2)  # Pole
            if progress >= 2:
                pygame.draw.line(self.preview_surface, (255, 255, 255),
                               (60, 20), (80, 20), 2)  # Top
                pygame.draw.line(self.preview_surface, (255, 255, 255),
                               (80, 20), (80, 30), 2)  # Rope
            if progress >= 3:
                pygame.draw.circle(self.preview_surface, (255, 255, 255),
                                 (80, 40), 10, 2)  # Head
            if progress >= 4:
                pygame.draw.line(self.preview_surface, (255, 255, 255),
                               (80, 50), (80, 70), 2)  # Body
            if progress >= 5:
                pygame.draw.line(self.preview_surface, (255, 255, 255),
                               (80, 55), (70, 65), 2)  # Left arm
                pygame.draw.line(self.preview_surface, (255, 255, 255),
                               (80, 55), (90, 65), 2)  # Right arm
            if progress >= 6:
                pygame.draw.line(self.preview_surface, (255, 255, 255),
                               (80, 70), (70, 85), 2)  # Left leg
                pygame.draw.line(self.preview_surface, (255, 255, 255),
                               (80, 70), (90, 85), 2)  # Right leg
                               
        elif game_name == "Pong":
            # Update ball position
            ball_x = 60 + int(30 * math.sin(self.animation_counter * 0.1))
            ball_y = 60 + int(20 * math.cos(self.animation_counter * 0.1))
            
            # Update AI paddle to follow ball
            if self.ai_paddle_y + 15 < ball_y:
                self.ai_paddle_y += 2
            elif self.ai_paddle_y + 15 > ball_y:
                self.ai_paddle_y -= 2
            
            # Update player paddle to create interesting gameplay
            target_y = 60 + int(25 * math.sin(self.animation_counter * 0.05))
            if self.player_paddle_y + 15 < target_y:
                self.player_paddle_y += 2
            elif self.player_paddle_y + 15 > target_y:
                self.player_paddle_y -= 2
            
            # Keep paddles in bounds
            self.ai_paddle_y = max(0, min(self.ai_paddle_y, 90))
            self.player_paddle_y = max(0, min(self.player_paddle_y, 90))
            
            # Draw paddles
            pygame.draw.rect(self.preview_surface, (255, 255, 255),
                           (10, self.player_paddle_y, 5, 30))  # Left paddle
            pygame.draw.rect(self.preview_surface, (255, 255, 255),
                           (105, self.ai_paddle_y, 5, 30))  # Right paddle
            
            # Draw ball with trail effect
            for i in range(3):
                trail_x = 60 + int(30 * math.sin((self.animation_counter - i*2) * 0.1))
                trail_y = 60 + int(20 * math.cos((self.animation_counter - i*2) * 0.1))
                alpha = 100 - i * 30
                trail = pygame.Surface((6, 6))
                trail.fill((255, 255, 255))
                trail.set_alpha(alpha)
                self.preview_surface.blit(trail, (trail_x - 3, trail_y - 3))
            
            pygame.draw.rect(self.preview_surface, (255, 255, 255),
                           (ball_x - 3, ball_y - 3, 6, 6))  # Ball
            
            # Draw center line
            for y in range(0, 120, 10):
                pygame.draw.rect(self.preview_surface, (128, 128, 128),
                               (58, y, 4, 4))
                               
        elif game_name == "Tetris":
            # Tetris pieces with their colors
            pieces = [
                ([(0, 0), (0, 1), (0, 2), (0, 3)], (0, 255, 255)),  # I
                ([(0, 0), (1, 0), (0, 1), (1, 1)], (255, 255, 0)),  # O
                ([(0, 0), (1, 0), (1, 1), (2, 1)], (255, 0, 0)),    # Z
                ([(0, 0), (0, 1), (0, 2), (1, 2)], (255, 165, 0))   # L
            ]
            
            # Update falling piece
            self.fall_counter += 1
            if self.fall_counter >= 20:
                self.fall_counter = 0
                self.piece_y += 1
                if self.piece_y > 8:
                    self.piece_y = -2
                    self.current_piece = (self.current_piece + 1) % len(pieces)
            
            # Draw game border
            pygame.draw.rect(self.preview_surface, (128, 128, 128),
                           (30, 10, 60, 100), 2)
            
            # Draw current falling piece
            piece, color = pieces[self.current_piece]
            for block in piece:
                x, y = block
                pygame.draw.rect(self.preview_surface, color,
                               (40 + x * 10, 20 + (y + self.piece_y) * 10, 8, 8))
            
            # Draw some fixed pieces at the bottom
            fixed_blocks = [
                (40, 90, (255, 0, 0)),
                (50, 90, (255, 0, 0)),
                (60, 90, (0, 255, 0)),
                (70, 90, (0, 255, 0)),
                (40, 80, (0, 255, 255)),
                (50, 80, (0, 255, 255)),
                (60, 80, (255, 165, 0))
            ]
            for x, y, color in fixed_blocks:
                pygame.draw.rect(self.preview_surface, color, (x, y, 8, 8))
        
        # Draw preview border
        pygame.draw.rect(self.preview_surface, (128, 128, 128),
                        (0, 0, self.preview_size[0], self.preview_size[1]), 1)
        
        # Draw the preview at the specified position
        screen.blit(self.preview_surface, position) 