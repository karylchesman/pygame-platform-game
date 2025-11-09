from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame


class TileMap:
    def __init__(self, game: Game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {}
        self.off_grid_tiles = []

        for i in range(10):
            self.tile_map[str(3 + i) + ";10"] = {
                "type": "grass",
                "variant": 1,
                "pos": (3 + i, 10),
            }
            self.tile_map["10;" + str(5 + i)] = {
                "type": "stone",
                "variant": 1,
                "pos": (10, 5 + i),
            }

    def render(self, surf: pygame.Surface):
        for tile in self.off_grid_tiles:
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                tile["pos"],
            )

        for location in self.tile_map:
            tile = self.tile_map[location]
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size),
            )
