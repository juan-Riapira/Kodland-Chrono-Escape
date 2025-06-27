import pygame
import os
import csv
from config import TILE_SIZE
from game.tiles import Tile
from game.player import Player
from game.enemy import Enemy

class LevelLoader:
    """
    Clase responsable de cargar niveles desde archivos CSV.
    
    Los archivos deben estar en formato CSV, donde cada carácter representa un objeto del nivel:
    - '1': Tile normal (bloque del suelo).
    - 'F': Tile de meta/fin de nivel.
    - 'P': Posición del jugador.
    - 'E': Enemigo.
    """

    def __init__(self, level_dir="levels"):
        """
        Inicializa el cargador de niveles.

        """
        self.level_dir = level_dir
        os.makedirs(level_dir, exist_ok=True)

    def load(self, filename):
        """
        Carga un nivel desde un archivo CSV y devuelve los elementos del juego.

        Returns:
            tuple: (tiles, player, enemies)
                - tiles (pygame.sprite.Group): Grupo de bloques del nivel.
                - player (Player): Objeto jugador.
                - enemies (pygame.sprite.Group): Grupo de enemigos.
        """
        tiles = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player = None

        path = os.path.join(self.level_dir, filename)
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for y, row in enumerate(reader):
                for x, tile in enumerate(row):
                    x_pos = x * TILE_SIZE
                    y_pos = y * TILE_SIZE

                    if tile == '1':
                        tiles.add(Tile(x_pos, y_pos))
                    elif tile == 'F':
                        tiles.add(Tile(x_pos, y_pos, is_finish=True))
                    elif tile == 'P':
                        player = Player(x_pos, y_pos)
                    elif tile == 'E':
                        enemies.add(Enemy(x_pos, y_pos))

        return tiles, player, enemies
