import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = [random.randint(-3, 3), random.randint(-3, 3)]
        self.timer = 30

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
