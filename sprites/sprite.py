import pygame

class Sprite:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
    
    def render(self, wd: pygame.Surface) -> None:
        pass
    
    def handle_event(self, event: pygame.event.Event) -> None:
        pass