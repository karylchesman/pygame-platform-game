import pygame

BASE_IMG_PATH = "data/images"


def load_image(path: str) -> pygame.Surface:
    img = pygame.image.load(f"{BASE_IMG_PATH}/{path}").convert()
    img.set_colorkey((0, 0, 0))
    return img
