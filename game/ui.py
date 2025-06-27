import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def draw_health_bar(self, surface, x, y, health, max_health):
        ratio = health / max_health
        pygame.draw.rect(surface, (255, 0, 0), (x, y, 200, 20))  # fondo rojo
        pygame.draw.rect(surface, (0, 255, 0), (x, y, 200 * ratio, 20))  # barra verde
        pygame.draw.rect(surface, (255, 255, 255), (x, y, 200, 20), 2)  # borde blanco

    def draw_level_indicator(self, surface, level):
        """Muestra el nivel actual en la pantalla"""
        level_text = self.small_font.render(f"Nivel: {level}", True, (255, 255, 255))
        surface.blit(level_text, (10, 40))

    def draw_main_menu(self, surface):
        surface.fill((10, 10, 10))
        title = self.big_font.render("Chrono Escape", True, (0, 255, 255))
        prompt = self.font.render("Presiona ENTER para jugar", True, (255, 255, 255))
        quit_prompt = self.font.render("ESC para salir", True, (180, 180, 180))

        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 150))
        surface.blit(prompt, (surface.get_width() // 2 - prompt.get_width() // 2, 250))
        surface.blit(quit_prompt, (surface.get_width() // 2 - quit_prompt.get_width() // 2, 300))

    def draw_pause_menu(self, surface):
        """Dibuja el menú de pausa"""
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render("PAUSA", True, (255, 255, 255))
        continue_text = self.font.render("Presiona ESC para continuar", True, (255, 255, 255))
        
        surface.blit(pause_text, (surface.get_width() // 2 - pause_text.get_width() // 2, 220))
        surface.blit(continue_text, (surface.get_width() // 2 - continue_text.get_width() // 2, 280))

    def draw_game_over_menu(self, surface):
        """Dibuja el menú de game over con opciones"""
        surface.fill((0, 0, 0))
        game_over_text = self.big_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = self.font.render("Presiona ENTER para reiniciar", True, (255, 255, 255))
        quit_text = self.font.render("Presiona ESC para salir", True, (180, 180, 180))

        surface.blit(game_over_text, (surface.get_width() // 2 - game_over_text.get_width() // 2, 200))
        surface.blit(restart_text, (surface.get_width() // 2 - restart_text.get_width() // 2, 260))
        surface.blit(quit_text, (surface.get_width() // 2 - quit_text.get_width() // 2, 300))

    def draw_victory_menu(self, surface):
        """Dibuja el menú de victoria"""
        surface.fill((0, 50, 0))
        victory_text = self.big_font.render("¡VICTORIA!", True, (0, 255, 0))
        congrats_text = self.font.render("¡Has completado todos los niveles!", True, (255, 255, 255))
        restart_text = self.font.render("Presiona ENTER para jugar de nuevo", True, (255, 255, 255))
        quit_text = self.font.render("Presiona ESC para salir", True, (180, 180, 180))

        surface.blit(victory_text, (surface.get_width() // 2 - victory_text.get_width() // 2, 180))
        surface.blit(congrats_text, (surface.get_width() // 2 - congrats_text.get_width() // 2, 230))
        surface.blit(restart_text, (surface.get_width() // 2 - restart_text.get_width() // 2, 280))
        surface.blit(quit_text, (surface.get_width() // 2 - quit_text.get_width() // 2, 320))

# game/enemy.py