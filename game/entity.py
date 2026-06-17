from __future__ import annotations
import pyttsx3
from typing import List

engine: pyttsx3.Engine = pyttsx3.init()
voices: List[pyttsx3.voice.Voice] = engine.getProperty("voices")

for voice in voices:
    if any("vi" in lang.lower() for lang in voice.languages):
        engine.setProperty("voice", voice.id)

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
        if self.dead():
            self.death_trigger(f"{self.name} đã chết vì ngộ độc")
    
    def dead(self) -> bool:
        return self.hp <= 0
    
    def death_trigger(self, death_message: str) -> None:
        engine.say(death_message)
        engine.runAndWait()
    
    def respawn(self) -> None:
        pass