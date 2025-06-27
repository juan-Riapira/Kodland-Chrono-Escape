import pygame
import os

class AssetLoader:
    def __init__(self, base_path="assets"):
        self.base_path = base_path
        self.images = {}
        self.sounds = {}
        self.music = {}

    def load_image(self, key, path):
        image = pygame.image.load(os.path.join(self.base_path, path)).convert_alpha()
        self.images[key] = image
        return image

    def get_image(self, key):
        return self.images.get(key)

    def load_sound(self, key, path):
        sound = pygame.mixer.Sound(os.path.join(self.base_path, path))
        self.sounds[key] = sound
        return sound

    def get_sound(self, key):
        return self.sounds.get(key)

    def load_music(self, path):
        pygame.mixer.music.load(os.path.join(self.base_path, path))

    def play_music(self, loops=-1):
        pygame.mixer.music.play(loops)
