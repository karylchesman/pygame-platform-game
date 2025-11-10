from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import pygame


class PhysicsEntity:
    def __init__(self, game: Game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0.0, 0.0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tile_map, movement=(0, 0)):
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for tile_rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(tile_rect):
                if frame_movement[0] > 0:
                    entity_rect.right = tile_rect.left
                if frame_movement[0] < 0:
                    entity_rect.left = tile_rect.right
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for tile_rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(tile_rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = tile_rect.top
                if frame_movement[1] < 0:
                    entity_rect.top = tile_rect.bottom
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

    def render(self, surf: pygame.Surface):
        surf.blit(self.game.assets["player"], self.pos)
