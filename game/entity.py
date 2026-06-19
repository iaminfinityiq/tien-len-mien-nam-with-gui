from __future__ import annotations
from .voice import speak
import asyncio

class Entity:
    def __init__(self, name: str, hp: int, damage: int) -> None:
        self.name: str = name
        self.hp: int = hp
        self.damage: int = damage
        self.poisoned_damage: int = 0
    
    def attack(self, entity: Entity) -> None:
        entity.hp -= self.damage
    
    def before_turn(self) -> None:
        self.hp -= self.poisoned_damage
    
    def dead(self) -> bool:
        return self.hp <= 0
    
    def death_trigger(self, death_message: str) -> None:
        asyncio.run(speak(death_message))
    
    def respawn(self) -> None:
        pass