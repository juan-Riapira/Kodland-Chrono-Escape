import pygame
import os
from config import GRAVITY, PLAYER_SPEED

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        """
        Inicializa al jugador en una posición dada.
        """
        super().__init__()
        image_path = os.path.join("assets/players", "player.png")
        if os.path.exists(image_path):
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (30, 50))
        else:
            self.image = pygame.Surface((30, 50), pygame.SRCALPHA)
            self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.shoot_cooldown = 0
        self.bullets = pygame.sprite.Group()
        self.health = 100
        self.max_health = 100

    def move(self, tiles):
        """
        Maneja el movimiento del jugador y las colisiones con el entorno.
        """
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
            self.facing_right = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        self.vel_y += GRAVITY
        dy += self.vel_y

        self.on_ground = False
        for tile in tiles:
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:
                    dy = tile.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    dy = tile.rect.bottom - self.rect.top
                    self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        """
        Dispara una bala en la dirección en la que el jugador está mirando.
        """
        if self.shoot_cooldown == 0:
            bullet_x = self.rect.centerx
            bullet_y = self.rect.centery
            direction = 1 if self.facing_right else -1
            bullet = Bullet(bullet_x, bullet_y, direction)
            self.bullets.add(bullet)
            self.shoot_cooldown = 20

    def take_damage(self, amount):
        """
        Reduce la salud del jugador por el daño recibido.
        """
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_dead(self):
        """
        Verifica si el jugador ha muerto.
        """
        return self.health <= 0

    def check_enemy_collisions(self, enemies):
        """
        Verifica colisiones con enemigos y aplica daño.
        """
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.take_damage(1)

    def update(self, tiles, enemies):
        """
        Actualiza el estado del jugador.
        """
        self.move(tiles)
        self.check_enemy_collisions(enemies)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        self.bullets.update()

        # Detectar si el jugador cae fuera del mapa
        if self.rect.top > 1000:
            self.health = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        """
        Inicializa la bala en una posición y dirección específica.
        """
        super().__init__()
        self.image = pygame.Surface((10, 5), pygame.SRCALPHA)
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = direction * 10

    def update(self):
        """
        Mueve la bala en su dirección y la destruye si sale de la pantalla.
        """
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
