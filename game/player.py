from .entity import Entity

class Player(Entity):
    def __init__(self, name: str) -> None:
        super().__init__(name, 10000, 100)
        self.poison_damage: int = 10
        self.heal_amount: int = 10
    
    def attack(self, entity: Entity) -> None:
        super().attack(entity)
        if entity.dead():
            if isinstance(entity, Player):
                entity.death_trigger(f"{self.name} đã đánh {entity.name} đến chết")
            else:
                if entity.tower_owner is not None:
                    entity.death_trigger(f"{entity.tower_owner.name}, bạn đã mất tòa của {entity.name}")
                
                entity.death_trigger(f"{self.name}, bạn đã chiếm được tòa của {entity.name}")