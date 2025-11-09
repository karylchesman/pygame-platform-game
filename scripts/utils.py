import os

import pygame

BASE_IMG_PATH = "data/images"


def load_image(path: str) -> pygame.Surface:
    img = pygame.image.load(f"{BASE_IMG_PATH}/{path}").convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path: str):
    images = []
    for img_path in sorted(os.listdir(f"{BASE_IMG_PATH}/{path}")):
        images.append(load_image(f"{path}/{img_path}"))
    return images
