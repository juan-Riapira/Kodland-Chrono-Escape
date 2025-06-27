import pygame
from game.level_loader import LevelLoader
from game.camera import Camera
from game.assent_loader import AssetLoader
from game.ui import UI
from game.player import Player
from game.tiles import Tile
from config import TILE_SIZE

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Chrono Escape")
clock = pygame.time.Clock()

assets = AssetLoader()
ui = UI()
level_loader = LevelLoader()
camera = Camera(1600, 1200)
particles = pygame.sprite.Group()

try:          
    assets.load_music("music/Interstellar-Main-Theme-Extra-Extended-Soundtrack-by-Hans-Zimmer.ogg")
    assets.play_music()
except:
    print("🎵 Música no cargada o archivo no encontrado.")

def reset_game():
    """Reinicia el juego desde el nivel 1"""
    global current_level, tiles, player, enemies, level_width, paused, level_transition, game_over, game_won
    current_level = 1
    
    try:
        new_tiles, new_player, new_enemies = level_loader.load(f"level{current_level}.csv")
        if not new_player:
            raise ValueError("No se encontró el jugador en el archivo de nivel.")
        
        if 'tiles' in globals():
            tiles.empty()
        if 'enemies' in globals():
            enemies.empty()
            
        # Asignar nuevos valores
        tiles = new_tiles
        player = new_player
        enemies = new_enemies
        
        level_width = get_level_width(tiles)
        paused = False
        level_transition = False
        game_over = False
        game_won = False
    except Exception as e:
        # Usar valores por defecto si hay error
        tiles = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player = None
        level_width = 800

def get_level_width(tiles):
    """Calcula el ancho del nivel basado en las tiles"""
    if not tiles:
        return 0
    max_x = max(tile.rect.right for tile in tiles)
    return max_x

def check_level_completion():
    """Verifica si el jugador ha completado el nivel actual"""
    global current_level, level_transition, transition_timer, transition_text, level_width, game_won, player, tiles, enemies
    
    # Verificar que el jugador existe antes de verificar completar nivel
    if not player or player.is_dead():
        return
    
    if player.rect.right >= level_width and not level_transition:
        current_level += 1
        max_levels = 5  # Puedes cambiar esto según cuántos niveles tengas
        
        if current_level > max_levels:
            game_won = True
        else:
            # Configurar la transición de nivel
            level_transition = True
            transition_timer = 120  # 2 segundos a 60 FPS
            transition_text = f"NIVEL {current_level}"
            
            try:
                # Cargar el nuevo nivel
                new_tiles, new_player, new_enemies = level_loader.load(f"level{current_level}.csv")
                
                if new_player:
                    # Mantener estadísticas del jugador
                    old_health = player.health
                    old_max_health = player.max_health
                    
                    # Actualizar referencias globales
                    tiles.empty()
                    enemies.empty()
                    tiles.add(new_tiles)
                    enemies.add(new_enemies)
                    player = new_player
                    
                    # Restaurar estadísticas
                    player.health = old_health
                    player.max_health = old_max_health
                    
                    # Recalcular el ancho del nuevo nivel
                    level_width = get_level_width(tiles)
                    
                    # Posicionar al jugador al inicio del nuevo nivel
                    player.rect.x = TILE_SIZE
                    ground_tiles = [tile for tile in tiles if tile.rect.y == max(t.rect.y for t in tiles) ]
                    if ground_tiles:
                        player.rect.y = min(ground_tiles, key=lambda t: t.rect.x).rect.y - player.rect.height
                    
                    camera.update(player)
                else:
                    game_won = True 
            except Exception as e:
                game_won = True 

# Inicializar juego
current_level = 1
try:
    tiles, player, enemies = level_loader.load(f"level{current_level}.csv")
    if not player:
        raise ValueError("No se encontró el jugador en el archivo de nivel.")
    level_width = get_level_width(tiles)
except Exception as e:
    # Crear nivel básico si hay error
    tiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = Player(100, 400)  # Posición por defecto
    # Crear algunas tiles básicas
    for i in range(20):
        tiles.add(Tile(i * TILE_SIZE, 500))
    level_width = 20 * TILE_SIZE

# Estados del juego
main_menu = True
paused = False
running = True
level_transition = False
game_over = False
game_won = False
transition_timer = 0
transition_text = ""

while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if main_menu and event.key == pygame.K_RETURN:
                main_menu = False
            elif main_menu and event.key == pygame.K_ESCAPE:
                running = False
            elif (game_over or game_won) and event.key == pygame.K_RETURN:
                reset_game()
                main_menu = False
            elif (game_over or game_won) and event.key == pygame.K_ESCAPE:
                running = False
            elif not main_menu and not game_over and not game_won and event.key == pygame.K_ESCAPE:
                if not level_transition:
                    paused = not paused
            elif not main_menu and not paused and not level_transition and not game_over and not game_won and event.key == pygame.K_f:
                if player:  # Verificar que el jugador existe antes de disparar
                    player.shoot()

    if main_menu:
        ui.draw_main_menu(screen)

    elif game_over:
        ui.draw_game_over_menu(screen)

    elif game_won:
        ui.draw_victory_menu(screen)

    elif paused:
        ui.draw_pause_menu(screen)

    elif level_transition:
        # Mostrar pantalla de transición de nivel
        screen.fill((0, 0, 0))
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        # Título principal
        title_surface = font_large.render(transition_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
        screen.blit(title_surface, title_rect)
        
        # Subtítulo
        subtitle_surface = font_small.render("Preparándose...", True, (200, 200, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 20))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Reducir el timer de transición
        transition_timer -= 1
        if transition_timer <= 0:
            level_transition = False

    else:
        # Juego principal
        if player and not player.is_dead():
            player.update(tiles, enemies)

        
            # Actualizar enemigos
            for enemy in enemies:
                enemy.update()
                enemy.check_bullet_collisions(player.bullets)

            particles.update()
            camera.update(player)

            # Verificar completar nivel
            check_level_completion()
        
        if player.rect.top > screen.get_height() + 200:
            player.health = 0  #  Morir si cae demasiado abajo
        # Verificar si el jugador murió
        if player and player.is_dead():
            game_over = True
            continue

        # Dibujar solo si no estamos en transición
        if not level_transition:
            # Dibujar tiles
            for tile in tiles:
                screen.blit(tile.image, camera.apply(tile))
            
            # Dibujar enemigos
            for enemy in enemies:
                enemy.draw(screen, camera)
            
            # Dibujar balas
            if player:
                for bullet in player.bullets:
                    screen.blit(bullet.image, camera.apply(bullet))
            
            # Dibujar jugador
            if player:
                screen.blit(player.image, camera.apply(player))
                # Dibujar UI
                ui.draw_health_bar(screen, 10, 10, player.health, player.max_health)
            
            ui.draw_level_indicator(screen, current_level)
            
            # Dibujar partículas
            for particle in particles:
                screen.blit(particle.image, camera.apply(particle))

    pygame.display.flip()

pygame.quit()