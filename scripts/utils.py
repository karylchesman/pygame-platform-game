import os
from pathlib import Path

import pygame

BASE_IMG_PATH = Path(__file__).parent.parent / "data" / "images"


def load_image(path: str) -> pygame.Surface:
    img = pygame.image.load(f"{BASE_IMG_PATH}/{path}").convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path: str):
    images = []
    for img_path in sorted(os.listdir(f"{BASE_IMG_PATH}/{path}")):
        images.append(load_image(f"{path}/{img_path}"))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_duration)
            return

        self.frame = min(self.frame + 1, len(self.images) * self.img_duration - 1)
        if self.frame >= len(self.images) * self.img_duration - 1:
            self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
