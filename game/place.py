from .entity import Entity
from .player import Player
from typing import List

class Place(Entity):
    def __init__(self, name: str, tower_owner: Player | None, players: List[Player]) -> None:
        super().__init__(name, 100000, 1000)
        self.tower_owner: Player | None = tower_owner
        self.players: List[Player] = players
        self.who_poisoned_last: Player | None = None
    
    def before_turn(self) -> None:
        super().before_turn()
        if self.dead():
            if self.tower_owner is not None:
                self.death_trigger(f"{self.tower_owner.name} đã mất tòa của {self.name}")
            
            if self.who_poisoned_last is not self.tower_owner and self.who_poisoned_last is not None:
                self.death_trigger(f"{self.who_poisoned_last.name} đã chiếm được tòa của {self.name}")
        
        if self.tower_owner is not None:
            for player in self.players:
                if player is not self.tower_owner:
                    self.damage(player)
                    if player.dead():
                        player.death_trigger(f"{player.name} đã gục ngã trước phòng thủ của {self.name}")