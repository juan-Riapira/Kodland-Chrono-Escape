import pygame
import os

class Enemy(pygame.sprite.Sprite):
    """
    Clase que representa un enemigo básico en el juego.
    """

    def __init__(self, x, y, enemy_type="basic"):
        """
        Inicializa un enemigo en la posición (x, y).

        """
        super().__init__()
        
        image_path = os.path.join("assets/players", "enemy.png")
        if os.path.exists(image_path):
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (30, 30))
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 0))  # Rojo por defecto

        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 50
        self.max_health = 50
        self.speed = 1
        self.direction = 1
        self.patrol_distance = 100
        self.start_x = x

    def update(self):
        """
        Actualiza la posición del enemigo con movimiento de patrullaje horizontal.
        Cambia de dirección al alcanzar los límites de patrulla.
        """
        self.rect.x += self.speed * self.direction
        
        if abs(self.rect.x - self.start_x) >= self.patrol_distance:
            self.direction *= -1

    def take_damage(self, amount):
        """
        Aplica daño al enemigo. Si la vida llega a 0, se elimina del juego.

        Args:
            amount (int): Cantidad de daño recibido.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def check_bullet_collisions(self, bullets):
        """
        Verifica colisiones con las balas del jugador.

        Args:
            bullets (pygame.sprite.Group): Grupo de balas.
        """
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                self.take_damage(25)
                bullet.kill()
                break

    def draw(self, surface, camera):
        """
        Dibuja el enemigo en pantalla, incluyendo su barra de vida.

        Args:
            surface (pygame.Surface): Superficie donde dibujar.
            camera (Camera): Cámara del juego para aplicar desplazamiento.
        """
        surface.blit(self.image, camera.apply(self))

        # Dibujar barra de vida encima del enemigo
        bar_width = 30
        bar_height = 4
        health_ratio = self.health / self.max_health

        camera_rect = camera.apply(self)
        bar_x = camera_rect.x
        bar_y = camera_rect.y - 8

        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height)) 
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)  
