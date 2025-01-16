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
        self.width = width
        self.height = height
        self.preview_size = (200, 150)
        
    def draw(self, surface, game_name, pos):
        preview = pygame.Surface(self.preview_size)
        preview.fill((40, 40, 40))
        
        if game_name == "Snake Game":
            self._draw_snake_preview(preview)
        elif game_name == "Hangman":
            self._draw_hangman_preview(preview)
        elif game_name == "Pong vs AI":
            self._draw_pong_preview(preview)
        elif game_name == "Tetris":
            self._draw_tetris_preview(preview)
            
        pygame.draw.rect(preview, (70, 70, 70), preview.get_rect(), 2)
        surface.blit(preview, pos)
        
    def _draw_snake_preview(self, surface):
        # Draw simple snake representation
        snake_color = (0, 255, 0)
        food_color = (255, 0, 0)
        block_size = 10
        
        # Draw snake body
        for i in range(5):
            pygame.draw.rect(surface, snake_color, 
                           (50 + i * block_size, 75, block_size - 1, block_size - 1))
        
        # Draw food
        pygame.draw.rect(surface, food_color, (100, 75, block_size - 1, block_size - 1))
        
    def _draw_hangman_preview(self, surface):
        # Draw gallows and stick figure
        pygame.draw.line(surface, (255, 255, 255), (50, 130), (150, 130), 2)  # Base
        pygame.draw.line(surface, (255, 255, 255), (100, 130), (100, 30), 2)  # Pole
        pygame.draw.line(surface, (255, 255, 255), (100, 30), (130, 30), 2)  # Top
        pygame.draw.line(surface, (255, 255, 255), (130, 30), (130, 50), 2)  # Rope
        
        # Draw stick figure
        pygame.draw.circle(surface, (255, 255, 255), (130, 60), 10, 2)  # Head
        pygame.draw.line(surface, (255, 255, 255), (130, 70), (130, 100), 2)  # Body
        pygame.draw.line(surface, (255, 255, 255), (130, 80), (115, 95), 2)  # Left arm
        pygame.draw.line(surface, (255, 255, 255), (130, 80), (145, 95), 2)  # Right arm
        pygame.draw.line(surface, (255, 255, 255), (130, 100), (115, 115), 2)  # Left leg
        pygame.draw.line(surface, (255, 255, 255), (130, 100), (145, 115), 2)  # Right leg
        
    def _draw_pong_preview(self, surface):
        # Draw paddles and ball
        pygame.draw.rect(surface, (255, 255, 255), (20, 50, 10, 50))  # Left paddle
        pygame.draw.rect(surface, (255, 255, 255), (170, 50, 10, 50))  # Right paddle
        pygame.draw.circle(surface, (255, 255, 255), (100, 75), 5)  # Ball
        
        # Draw center line
        for y in range(0, self.preview_size[1], 20):
            pygame.draw.rect(surface, (255, 255, 255), (98, y, 4, 10))
            
    def _draw_tetris_preview(self, surface):
        # Draw some tetris pieces
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        block_size = 15
        
        # Draw a few random pieces
        shapes = [
            [(0, 0), (1, 0), (2, 0), (3, 0)],  # I piece
            [(0, 0), (1, 0), (0, 1), (1, 1)],  # O piece
            [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z piece
        ]
        
        for i, shape in enumerate(shapes):
            color = colors[i % len(colors)]
            for x, y in shape:
                pygame.draw.rect(surface, color,
                               (50 + x * block_size, 40 + y * block_size + i * 30,
                                block_size - 1, block_size - 1)) 