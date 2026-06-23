from __future__ import annotations
from .entity import Entity
from .player import Player
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player

class Place(Entity):
    def __init__(self, name: str, tower_owner: Player | None, players: List[Player], previous: Place | None, next: Place | None) -> None:
        super().__init__(name, 100000, 1000)
        self.tower_owner: Player | None = tower_owner
        self.players: List[Player] = players
        self.who_poisoned_last: Player | None = None
        self.previous: Place | None = previous
        self.next: Place | None = next
    
    def before_turn(self) -> None:
        super().before_turn()
        if self.dead():
            self.switch_tower_owner(self.who_poisoned_last)
        
        if self.tower_owner is not None:
            for player in self.players:
                if player is not self.tower_owner:
                    self.attack(player)
                    if player.dead():
                        player.death_trigger(f"{player.name} đã gục ngã trước phòng thủ của {self.name}")
    
    def switch_tower_owner(self, last_attacked: Player | None) -> None:
        if self.tower_owner is not None:
            self.death_trigger(f"{self.tower_owner.name} đã mất tòa của {self.name}")
        
        if last_attacked is not self.tower_owner and last_attacked is not None:
            self.death_trigger(f"{self.who_poisoned_last.name} đã chiếm được tòa của {self.name}")
            self.tower_owner = last_attacked
        else:
            self.tower_owner = None
    
    def respawn(self) -> None:
        self.hp = 100000
    
    def death_trigger(self, death_message: str) -> None:
        super().death_trigger(death_message)
        self.respawn()