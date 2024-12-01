import numpy as np
import pygame

class Sound:
    def __init__(self):
        # initilize 16-bit mono sound
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        self.buzz = self.generate_beep()

    def generate_beep(self, frequency=440, duration=0.2, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        wave = (wave * 32767).astype(np.int16)  # Convert to 16-bit PCM format
        sound = pygame.sndarray.make_sound(wave)
        return sound

    def play(self):
        self.buzz.play()

