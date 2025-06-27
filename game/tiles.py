
import pygame
from config import TILE_SIZE

class Tile(pygame.sprite.Sprite):
    
    def __init__(self, x, y, is_finish=False):
        """
        Inicializa una tile en la posición especificada.
        """
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((100, 100, 100) if not is_finish else (0, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_finish = is_finish
