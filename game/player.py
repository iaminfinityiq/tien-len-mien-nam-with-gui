from __future__ import annotations
from .entity import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .place import Place

class Player(Entity):
    def __init__(self, name: str) -> None:
        super().__init__(name, 10000, 100)
        self.poison_damage: int = 10
        self.heal_amount: int = 10
        self.death_time: int = 0
        self.max_hp: int = 10000
        self.at: Place | None = None
        self.at_home_tower: int = 0
    
    def attack(self, entity: Entity) -> None:
        super().attack(entity)
        if entity.dead():
            if isinstance(entity, Player):
                entity.death_trigger(f"{self.name} đã đánh {entity.name} đến chết")
            else:
                if entity.tower_owner is not None:
                    entity.death_trigger(f"{entity.tower_owner.name}, bạn đã mất tòa của {entity.name}")
                
                entity.death_trigger(f"{self.name}, bạn đã chiếm được tòa của {entity.name}")
    
    def before_turn(self) -> None:
        if self.dead():
            self.death_time -= 1
            if self.death_time == 0:
                self.respawn()
        else:
            super().before_turn()
            if self.dead():
                self.death_trigger(f"{self.name} đã chết vì ngộ độc")
            elif self.at.tower_owner is self:
                self.at_home_tower += 1
            else:
                self.at_home_tower = 0
    
    def respawn(self) -> None:
        self.hp = self.max_hp
        self.at_home_tower = 0
        super().death_trigger(f"{self.name} đã hồi sinh")
    
    def death_trigger(self, death_message: str) -> None:
        self.death_time = 10
        self.at.players.remove(self)
        self.at = None
        super().death_trigger(death_message)