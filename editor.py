import sys

import pygame

from scripts.utils import load_images
from scripts.tilemap import TileMap

RENDER_SCALE = 2.0


class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Ninja Game - Editor")

        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            "decor": load_images("/tiles/decor"),
            "grass": load_images("/tiles/grass"),
            "large_decor": load_images("/tiles/large_decor"),
            "stone": load_images("/tiles/stone"),
        }
        self.movement = [False, False, False, False]

        self.tile_map = TileMap(self, tile_size=16)
        self.scroll = [0.0, 0.0]

        self.tiles_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift_held = False

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            render_scroll = [int(self.scroll[0]), int(self.scroll[1])]

            self.tile_map.render(self.display, render_scroll)

            current_tile_img = self.assets[self.tiles_list[self.tile_group]][
                self.tile_variant
            ].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (
                int((mpos[0] + render_scroll[0]) // self.tile_map.tile_size),
                int((mpos[1] + render_scroll[1]) // self.tile_map.tile_size),
            )

            if self.clicking:
                self.tile_map.tile_map[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {
                    "type": self.tiles_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": (tile_pos[0], tile_pos[1]),
                }
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                if tile_loc in self.tile_map.tile_map:
                    del self.tile_map.tile_map[tile_loc]

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # left click
                    if event.button == 1:
                        self.clicking = True
                    # right click
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift_held:
                        current_tile_group = self.assets[
                            self.tiles_list[self.tile_group]
                        ]
                        # scroll up
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                current_tile_group
                            )
                        # scroll down
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                current_tile_group
                            )
                    else:
                        # scroll up
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(
                                self.tiles_list
                            )
                            self.tile_variant = 0
                        # scroll down
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(
                                self.tiles_list
                            )
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    # left click
                    if event.button == 1:
                        self.clicking = False
                    # right click
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift_held = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift_held = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Editor().run()
