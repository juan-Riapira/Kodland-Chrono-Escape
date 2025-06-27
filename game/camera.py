import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, width, height):
        # Define el rectángulo de visión de la cámara
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, target):
        # Desplaza el rect del objeto según el offset de la cámara
        return target.rect.move(self.camera_rect.topleft)

    def update(self, target):
        # Centrar horizontalmente y verticalmente al jugador
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        # Limitar para que la cámara no muestre fuera de los bordes del mapa
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)

        # Actualiza el rect de la cámara
        self.camera_rect = pygame.Rect(x, y, self.width, self.height)
