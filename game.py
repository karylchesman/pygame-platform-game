import sys

import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import TileMap
from scripts.clouds import Clouds


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Ninja Game")

        # The 'screen' is the actual window, while 'display' is the internal rendering surface,
        # the idea is to render everything to 'display' and then scale it up to 'screen'
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]
        self.assets = {
            "decor": load_images("/tiles/decor"),
            "grass": load_images("/tiles/grass"),
            "large_decor": load_images("/tiles/large_decor"),
            "stone": load_images("/tiles/stone"),
            "player": load_image("/entities/player.png"),
            "background": load_image("/background.png"),
            "clouds": load_images("/clouds"),
            "player/idle": Animation(load_images("/entities/player/idle"), img_dur=6),
            "player/run": Animation(load_images("/entities/player/run"), img_dur=4),
            "player/jump": Animation(load_images("/entities/player/jump")),
            "player/slide": Animation(load_images("/entities/player/slide")),
            "player/wall_slide": Animation(load_images("/entities/player/wall_slide")),
        }
        self.clouds = Clouds(self.assets["clouds"], count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tile_map = TileMap(self, tile_size=16)
        self.scroll = [0.0, 0.0]

    def run(self):
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            self.scroll[0] += (
                # The X position of the center of the player in the world, not on display
                self.player.rect().centerx
                # The camera is positioned in the top-left corner, so we subtract half the display width
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            print(render_scroll)
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            self.tile_map.render(self.display, offset=render_scroll)

            self.player.update(self.tile_map, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
