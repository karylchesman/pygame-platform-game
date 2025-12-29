from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import json
import pygame

NEIGHBOR_OFFSETS = [
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (0, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]

PHYSICS_TILES = {"grass", "stone"}
AUTO_TILE_TYPES = {"grass", "stone"}
AUTO_TILE_RULE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}


class TileMap:
    def __init__(self, game: Game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {}
        self.off_grid_tiles = []

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.off_grid_tiles.copy():
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.off_grid_tiles.remove(tile)
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                # this line bellow is because we store the position of a tile as tile coordinates
                # and we want the position in this method as pixel coordinates but we don't want to modify the original tile data
                matches[-1]["pos"] = matches[-1]["pos"].copy()
                matches[-1]["pos"][0] *= self.tile_size
                matches[-1]["pos"][1] *= self.tile_size
                if not keep:
                    del self.tile_map[loc]
        return matches

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = (
                str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
            )
            if check_loc in self.tile_map:
                tiles.append(self.tile_map[check_loc])
        return tiles

    def solid_check(self, pos):
        tile_loc = (
            str(int(pos[0] // self.tile_size))
            + ";"
            + str(int(pos[1] // self.tile_size))
        )
        if tile_loc in self.tile_map:
            if self.tile_map[tile_loc]["type"] in PHYSICS_TILES:
                return self.tile_map[tile_loc]
        return None

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(
                    pygame.Rect(
                        tile["pos"][0] * self.tile_size,
                        tile["pos"][1] * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                )
        return rects

    def auto_tile(self):
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = (
                    str(tile["pos"][0] + shift[0])
                    + ";"
                    + str(tile["pos"][1] + shift[1])
                )
                if check_loc in self.tile_map:
                    if self.tile_map[check_loc]["type"] == tile["type"]:
                        neighbors.add(shift)
            neighbors_tuple = tuple(sorted(neighbors))
            if (tile["type"] in AUTO_TILE_TYPES) and (
                neighbors_tuple in AUTO_TILE_RULE_MAP
            ):
                tile["variant"] = AUTO_TILE_RULE_MAP[neighbors_tuple]

    def render(self, surf: pygame.Surface, offset=(0, 0)):
        for tile in self.off_grid_tiles:
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )

        for x in range(
            offset[0] // self.tile_size,
            (offset[0] + surf.get_width()) // self.tile_size + 1,
        ):
            for y in range(
                offset[1] // self.tile_size,
                (offset[1] + surf.get_height()) // self.tile_size + 1,
            ):
                tile_key = str(x) + ";" + str(y)
                if tile_key in self.tile_map:
                    tile = self.tile_map[tile_key]
                    surf.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (
                            tile["pos"][0] * self.tile_size - offset[0],
                            tile["pos"][1] * self.tile_size - offset[1],
                        ),
                    )

        # for tile in self.tile_map.values():
        #     surf.blit(
        #         self.game.assets[tile["type"]][tile["variant"]],
        #         (
        #             tile["pos"][0] * self.tile_size - offset[0],
        #             tile["pos"][1] * self.tile_size - offset[1],
        #         ),
        #     )

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(
                {
                    "tilemap": self.tile_map,
                    "tile_size": self.tile_size,
                    "offgrid": self.off_grid_tiles,
                },
                f,
            )

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
            self.tile_map = data["tilemap"]
            self.tile_size = data["tile_size"]
            self.off_grid_tiles = data["offgrid"]
