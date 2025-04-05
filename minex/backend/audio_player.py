import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from concurrent.futures import ThreadPoolExecutor
import pygame

class AudioPlayer:
    def __init__(self, sound_folder):
        pygame.mixer.init()
        self.sounds = {}
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._load(sound_folder)
        self.disabled = True

    def _load(self, folder):
        for file_name in os.listdir(folder):
            if file_name.endswith((".ogg", ".mp3", ".wav")):
                sound_name = os.path.splitext(file_name)[0]
                file_path = os.path.join(folder, file_name)
                self.sounds[sound_name] = pygame.mixer.Sound(file_path)

    def play(self, name):
        if name in self.sounds and not self.disabled:
            self.executor.submit(self.sounds[name].play)
