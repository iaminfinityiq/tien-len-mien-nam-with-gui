import pygame
from sprites.textbox import TextBox

pygame.init()

wd: pygame.Surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Tiến lên Miền Nam 2", "TLMN2")
clock: pygame.time.Clock = pygame.time.Clock()

running: bool = True
event_number: int = 0
p1_textbox: TextBox = TextBox(36, 16, 290, 26, pygame.Color(255, 0, 0), pygame.Color(0, 0, 0), "Consolas", 16, 30)
p2_textbox: TextBox = TextBox(36, 47, 290, 26, pygame.Color(0, 0, 255), pygame.Color(0, 0, 0), "Consolas", 16, 30)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if event_number <= 1 or event_number >= 3:
                    event_number += 1
                elif event_number == 2 and p1_textbox.text != "" and p2_textbox.text != "":
                    event_number += 1
            elif event_number == 2:
                p1_textbox.handle_event(event)
                p2_textbox.handle_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event_number == 2:
                p1_textbox.handle_event(event)
                p2_textbox.handle_event(event)
    
    wd.fill(pygame.Color(255, 255, 255))
    if event_number == 0:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Chào mừng đến với Tiến lên Miền Nam", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))
        
        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 16))
    elif event_number == 1:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Trước tiên, trò này cần có 2 người chơi", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 16))
    elif event_number == 2:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Trước tiên, trò này cần có 2 người chơi", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render("P1:", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 21))

        text_surface = pygame.font.SysFont("Consolas", 16).render("P2:", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 51))

        p1_textbox.render(wd)
        p2_textbox.render(wd)

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 87))
    elif event_number == 3:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Trước tiên, trò này cần có 2 người chơi", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render(f"P1: {p1_textbox.text}", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 21))

        text_surface = pygame.font.SysFont("Consolas", 16).render(f"P2: {p2_textbox.text}", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 51))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 67))
    elif event_number == 4:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Chúng ta sẽ chơi trên bản đồ sau:", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        pygame.draw.rect(wd, pygame.Color(135, 206, 250), pygame.Rect(50, 50, 100, 100))
        pygame.draw.rect(wd, pygame.Color(140, 255, 155), pygame.Rect(200, 50, 100, 100))
        pygame.draw.rect(wd, pygame.Color(128, 128, 128), pygame.Rect(350, 50, 100, 100))
        pygame.draw.rect(wd, pygame.Color(128, 128, 128), pygame.Rect(500, 50, 100, 100))
        pygame.draw.rect(wd, pygame.Color(128, 128, 128), pygame.Rect(650, 50, 100, 100))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Hà Nội", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (73, 92))
        
        text_surface = pygame.font.SysFont("Consolas", 16).render("Thanh Hóa", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (209, 92))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Huế", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (386, 92))
        
        text_surface = pygame.font.SysFont("Consolas", 16).render("Đắk Lắk", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (518, 92))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Sài Gòn", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (668, 92))

        pygame.draw.rect(wd, pygame.Color(155, 118, 83), pygame.Rect(150, 90, 50, 20))
        pygame.draw.rect(wd, pygame.Color(155, 118, 83), pygame.Rect(300, 90, 50, 20))
        pygame.draw.rect(wd, pygame.Color(155, 118, 83), pygame.Rect(450, 90, 50, 20))
        pygame.draw.rect(wd, pygame.Color(155, 118, 83), pygame.Rect(600, 90, 50, 20))
    
    pygame.display.flip()