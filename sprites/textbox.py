from .sprite import Sprite
import pygame

class TextBox(Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, bg_color: pygame.Color, fg_color: pygame.Color, font: str, font_size: int, character_limit: int) -> None:
        super().__init__(x, y, width, height)
        self.bg_color: int = bg_color
        self.fg_color: int = fg_color
        self.text: str = ""
        self.font: pygame.font.Font = pygame.font.SysFont(font, font_size)
        self.font_size: int = font_size
        self.active: bool = False
        self.character_limit: int = character_limit
    
    def render(self, wd: pygame.Surface) -> None:
        rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(wd, self.bg_color, rect)

        text_surface: pygame.Surface = self.font.render(self.text, True, self.fg_color)
        wd.blit(text_surface, (self.x + 10, self.y + self.height // 2 - self.font_size // 2))
    
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            self.active = self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
        
        if event.type == pygame.TEXTINPUT:
            if self.active:
                self.text += event.text