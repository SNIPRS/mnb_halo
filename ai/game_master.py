import pygame

import G
from ai.character_ai import EnemyCharacterAI, ControllableCharacterAI

class EnemyManager:
    def __init__(self):
        self.max_cleanup_timer = G.FPS * 10
        self.cleanup_timer = self.max_cleanup_timer
        self._spawn_enemy()
        self._spawn_enemy()

    def frame(self):
        self.cleanup_timer -= 1
        for c in G.CHAR_AI_ALL:
            c.frame()
        if self.cleanup_timer <= 0:
            self._cleanup()
            self.cleanup_timer = self.max_cleanup_timer

    def _spawn_enemy(self):
        enemy = EnemyCharacterAI()
        G.CHAR_AI_ALL.add(enemy)

    def _cleanup(self):
        print('cleanup')
        for c in G.CHAR_AI_ALL:
            if c.can_kill():
                c.kill()
                self._spawn_enemy()


