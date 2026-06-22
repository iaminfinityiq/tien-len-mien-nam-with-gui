from .place import Place
from .player import Player
from typing import List, Dict, Tuple
import pygame
from .voice import speak
import asyncio

def integer_to_text(n: int) -> str:
    if n < 1000:
        return str(n)

    if n < 1_000_000:
        return f"{n / 1000:.1f}K"

    if n < 1_000_000_000:
        return f"{n / 1_000_000:.1f}M"

    if n < 1_000_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"

    if n < 1_000_000_000_000_000:
        return f"{n / 1_000_000_000_000:.1f}T"

    return "999.9T+"

class Game:
    def __init__(self, p1_name: str, p2_name: str) -> None:
        self.players: List[Player] = [Player(p1_name), Player(p2_name)]
        self.map: Place = self.map_generation()
        self.turn: int = 1
    
    def map_generation(self) -> Place:
        hanoi: Place = Place("Hà Nội", self.players[0], [self.players[0]], None, None)
        thanh_hoa: Place = Place("Thanh Hóa", self.players[0], [], None, None)
        hue: Place = Place("Huế", None, [], None, None)
        daklak: Place = Place("Đắk Lắk", self.players[1], [], None, None)
        saigon: Place = Place("Sài Gòn", self.players[1], [self.players[1]], None, None)
        self.players[0].at = hanoi
        self.players[1].at = saigon

        self.spawn_points: List[Place] = [hanoi, saigon]
        self.player_y_dict: Dict[Place, int] = {
            hanoi: 450,
            thanh_hoa: 350,
            hue: 350,
            daklak: 420,
            saigon: 420
        }
        
        hanoi.next = thanh_hoa
        thanh_hoa.previous = hanoi

        thanh_hoa.next = hue
        hue.previous = thanh_hoa

        hue.next = daklak
        daklak.previous = hue

        daklak.next = saigon
        saigon.previous = daklak

        return self.spawn_points[0]
    
    def before_turn(self) -> None:
        if self.spawn_points[0].dead() and self.spawn_points[1].dead():
            self.spawn_points[0].death_trigger("Cả 2 tòa của Hà Nội và Sài Gòn đã bị phá hủy cùng một lúc, cả hai đội đều hòa")
        elif self.spawn_points[0].dead():
            self.spawn_points[0].death_trigger(f"Tháp của Hà Nội đã bị phá hủy, {self.players[1].name} đã giành chiến thắng!")
        elif self.spawn_points[1].dead():
            self.spawn_points[1].death_trigger(f"Tháp của Sài Gòn đã bị phá hủy, {self.players[0].name} đã giành chiến thắng!")

        for i, player in enumerate(self.players):
            past_death_time: int = player.death_time
            player.before_turn()
            if past_death_time == 1:
                player.at = self.spawn_points[i]
                self.spawn_points[i].players += [player]
        
        current: Place = self.map
        while current != None:
            current.before_turn()
            current = current.next
    
    def after_turn(self) -> None:
        self.turn = 1 - self.turn
        asyncio.run(speak(f"Đang là lượt của {self.players[self.turn].name}"))

    def render_scene(self, wd: pygame.Surface, scene: Place) -> None:
        if scene is None:
            text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render(f"{self.players[self.turn].name}, bạn đã chết, vui lòng đợi một lát để được hồi sinh", True, pygame.Color(0, 0, 0))
            wd.blit(text_surface, (0, 0))

            text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render(f"Nhấn bất kỳ đâu trên màn hình để tiếp tục...", True, pygame.Color(0, 0, 0))
            wd.blit(text_surface, (0, 16))
            return
        
        if scene.name == "Hà Nội":
            wd.fill(pygame.Color(135, 206, 250))
            pygame.draw.circle(wd, pygame.Color(255, 255, 0), (800, 0), 200)
            pygame.draw.rect(wd, pygame.Color(80, 180, 80), pygame.Rect(0, 550, 800, 250))
            pygame.draw.rect(wd, pygame.Color(180, 180, 180), pygame.Rect(250, 380, 300, 170))
            pygame.draw.polygon(wd, pygame.Color(150, 150, 150), [(230, 380), (570, 380), (520, 340), (280, 340)])

            if scene.tower_owner is None:
                pygame.draw.circle(wd, pygame.Color(128, 128, 128), (400, 465), 20)
            elif scene.tower_owner is self.players[self.turn]:
                pygame.draw.circle(wd, pygame.Color(0, 0, 255), (400, 465), 20)
            else:
                pygame.draw.circle(wd, pygame.Color(255, 0, 0), (400, 465), 20)
        elif scene.name == "Thanh Hóa":
            wd.fill(pygame.Color(140, 255, 155))
            pygame.draw.rect(wd, pygame.Color(80, 180, 80), pygame.Rect(0, 450, 800, 350))
            pygame.draw.rect(wd, pygame.Color(130, 130, 130), pygame.Rect(100, 250, 600, 200))
            pygame.draw.rect(wd, pygame.Color(70, 70, 70), pygame.Rect(300, 330, 200, 120))
            pygame.draw.arc(wd, pygame.Color(70, 70, 70), pygame.Rect(300, 210, 200, 240), 3.14, 0, 12)
            for x in range(100, 700, 48):
                pygame.draw.rect(wd, pygame.Color(110, 110, 110), pygame.Rect(x, 220, 24, 30))

            pygame.draw.line(wd, pygame.Color(80, 80, 80), (400, 180), (400, 250), 4)
            pygame.draw.polygon(wd, pygame.Color(255, 0, 0), [(400, 180), (460, 200), (400, 220)])
            if scene.tower_owner is None:
                pygame.draw.circle(wd, pygame.Color(128, 128, 128), (400, 390), 20)
            elif scene.tower_owner is self.players[self.turn]:
                pygame.draw.circle(wd, pygame.Color(0, 0, 255), (400, 390), 20)
            else:
                pygame.draw.circle(wd, pygame.Color(255, 0, 0), (400, 390), 20)
        elif scene.name == "Huế":
            wd.fill(pygame.Color(180, 220, 255))
            pygame.draw.rect(wd, pygame.Color(90, 170, 90), pygame.Rect(0, 500, 800, 300))
            pygame.draw.rect(wd, pygame.Color(50, 120, 255), pygame.Rect(0, 450, 800, 50))
            pygame.draw.rect(wd, pygame.Color(210, 180, 140), pygame.Rect(180, 250, 440, 200))
            pygame.draw.rect(wd, pygame.Color(90, 60, 40), pygame.Rect(325, 330, 150, 120))
            pygame.draw.rect(wd, pygame.Color(180, 120, 60), pygame.Rect(240, 170, 320, 80))
            pygame.draw.polygon(wd, pygame.Color(120, 40, 20), [(220, 170), (580, 170), (540, 130), (260, 130)])
            for x in (272, 352, 432, 512):
                pygame.draw.rect(wd, pygame.Color(140, 90, 50), pygame.Rect(x, 170, 15, 80))
            
            if scene.tower_owner is None:
                pygame.draw.circle(wd, pygame.Color(128, 128, 128), (400, 390), 20)
            elif scene.tower_owner is self.players[self.turn]:
                pygame.draw.circle(wd, pygame.Color(0, 0, 255), (400, 390), 20)
            else:
                pygame.draw.circle(wd, pygame.Color(255, 0, 0), (400, 390), 20)
        elif scene.name == "Đắk Lắk":
            wd.fill(pygame.Color(153, 0, 76))
            pygame.draw.rect(wd, pygame.Color(120, 0, 60), pygame.Rect(0, 250, 800, 600))
            pygame.draw.rect(wd, pygame.Color(90, 0, 50), pygame.Rect(0, 400, 800, 400))
            pygame.draw.rect(wd, pygame.Color(60, 0, 35), pygame.Rect(0, 520, 800, 280))
            for x in range(60, 800, 140):
                pygame.draw.circle(wd, pygame.Color(30, 0, 20), (x, 600), 28)
                pygame.draw.circle(wd, pygame.Color(25, 0, 15), (x + 40, 650), 20)

            for x in range(120, 800, 220):
                pygame.draw.polygon(wd, pygame.Color(200, 80, 0), [(x, 580), (x + 20, 520), (x + 40, 580)])
                pygame.draw.polygon(wd, pygame.Color(255, 140, 0), [(x + 10, 570), (x + 20, 540), (x + 30, 570)])

            for x in range(80, 800, 160):
                pygame.draw.rect(wd, pygame.Color(40, 40, 40), pygame.Rect(x, 280, 18, 260))

            pygame.draw.rect(wd, pygame.Color(20, 0, 15), pygame.Rect(480, 430, 170, 90))
            pygame.draw.rect(wd, pygame.Color(20, 0, 15), pygame.Rect(450, 460, 60, 40))
            pygame.draw.polygon(wd, pygame.Color(20, 0, 15), [(520, 430), (560, 390), (600, 430)])

            if scene.tower_owner is None:
                pygame.draw.circle(wd, pygame.Color(128, 128, 128), (565, 475), 20)
            elif scene.tower_owner is self.players[self.turn]:
                pygame.draw.circle(wd, pygame.Color(0, 0, 255), (565, 475), 20)
            else:
                pygame.draw.circle(wd, pygame.Color(255, 0, 0), (565, 475), 20)
        elif scene.name == "Sài Gòn":
            wd.fill(pygame.Color(102, 0, 51))
            pygame.draw.rect(wd, pygame.Color(80, 0, 40), pygame.Rect(0, 250, 800, 550))
            pygame.draw.rect(wd, pygame.Color(50, 20, 20), pygame.Rect(0, 520, 800, 280))
            pygame.draw.rect(wd, pygame.Color(220, 220, 180), pygame.Rect(220, 180, 360, 220))
            for y in range(220, 380, 40):
                pygame.draw.line(wd, pygame.Color(140, 140, 110), (220, y), (580, y), 2)

            pygame.draw.rect(wd, pygame.Color(100, 100, 100), pygame.Rect(340, 300, 120, 100))
            pygame.draw.line(wd, pygame.Color(80, 80, 80), (400, 120), (400, 180), 4)
            pygame.draw.rect(wd, pygame.Color(40, 90, 40), pygame.Rect(300, 430, 200, 70))
            pygame.draw.circle(wd, pygame.Color(50, 110, 50), (400, 465), 35)
            pygame.draw.rect(wd, pygame.Color(50, 110, 50), pygame.Rect(400, 455, 140, 12))
            pygame.draw.rect(wd, pygame.Color(20, 20, 20), pygame.Rect(290, 490, 220, 20))
            for x in range(320, 501, 45):
                pygame.draw.circle(wd, pygame.Color(60, 60, 60), (x, 500), 12)

            if scene.tower_owner is None:
                pygame.draw.circle(wd, pygame.Color(128, 128, 128), (400, 465), 20)
            elif scene.tower_owner is self.players[self.turn]:
                pygame.draw.circle(wd, pygame.Color(0, 0, 255), (400, 465), 20)
            else:
                pygame.draw.circle(wd, pygame.Color(255, 0, 0), (400, 465), 20)
        
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        if not self.players[0].dead() and self.players[0] in scene.players:
            if self.turn == 0:
                pygame.draw.rect(wd, pygame.Color(0, 0, 255), pygame.Rect(0, self.player_y_dict[scene], 100, 100))
            else:
                pygame.draw.rect(wd, pygame.Color(255, 0, 0), pygame.Rect(0, self.player_y_dict[scene], 100, 100))
            
            pygame.draw.rect(wd, pygame.Color(255, 127, 127), pygame.Rect(0, self.player_y_dict[scene] - 60, 100, 40))
            pygame.draw.rect(wd, pygame.Color(46, 204, 113), pygame.Rect(0, self.player_y_dict[scene] - 60, self.players[0].hp*100//self.players[0].max_hp, 20))
            pygame.draw.rect(wd, pygame.Color(0, 100, 0), pygame.Rect(0, self.player_y_dict[scene] - 40, min(self.players[0].poisoned_damage, self.players[0].max_hp)*100//self.players[0].max_hp, 20))
            if 0 <= mouse_pos[0] <= 100 and self.player_y_dict[scene] <= mouse_pos[1] <= self.player_y_dict[scene] + 100:
                pygame.draw.rect(wd, pygame.Color(128, 128, 128), pygame.Rect(100, self.player_y_dict[scene], 100, 200))
                text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render(f"HP: {integer_to_text(self.players[0].hp)}/{integer_to_text(self.players[0].max_hp)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (105, self.player_y_dict[scene] + 5))

                text_surface = pygame.font.SysFont("Consolas", 10, True).render(f"Công: {integer_to_text(self.players[0].damage)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (105, self.player_y_dict[scene] + 20))

                text_surface = pygame.font.SysFont("Consolas", 10, True).render(f"Độc: {integer_to_text(self.players[0].poison_damage)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (105, self.player_y_dict[scene] + 35))

                text_surface = pygame.font.SysFont("Consolas", 10, True).render(f"Hồi: {integer_to_text(self.players[0].heal_amount)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (105, self.player_y_dict[scene] + 50))

                text_surface = pygame.font.SysFont("Consolas", 10, True).render(f"Bị độc: {integer_to_text(self.players[0].poisoned_damage)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (105, self.player_y_dict[scene] + 65))
            
            if self.turn == 1 and self.players[0].at is self.players[1].at:
                pygame.draw.rect(wd, pygame.Color(255, 60, 60), pygame.Rect(0, self.player_y_dict[scene] - 80, 20, 20))
                pygame.draw.rect(wd, pygame.Color(0, 100, 0), pygame.Rect(80, self.player_y_dict[scene] - 80, 20, 20))
                if 0 <= mouse_pos[0] <= 20 and self.player_y_dict[scene] - 80 <= mouse_pos[1] <= self.player_y_dict[scene] - 60:
                    text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render("Tấn công", True, pygame.Color(0, 0, 0))
                    wd.blit(text_surface, (26, self.player_y_dict[scene] - 75))
                elif 80 <= mouse_pos[0] <= 100 and self.player_y_dict[scene] - 80 <= mouse_pos[1] <= self.player_y_dict[scene] - 60:
                    text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render("Đầu độc", True, pygame.Color(0, 0, 0))
                    wd.blit(text_surface, (29, self.player_y_dict[scene] - 75))
            
            if self.turn == 0 and self.players[0].at.tower_owner is self.players[0]:
                pygame.draw.rect(wd, pygame.Color(255, 60, 60), pygame.Rect(0, self.player_y_dict[scene] - 80, 20, 20))
                pygame.draw.rect(wd, pygame.Color(0, 100, 0), pygame.Rect(80, self.player_y_dict[scene] - 80, 20, 20))

                if 0 <= mouse_pos[0] <= 20 and self.player_y_dict[scene] - 80 <= mouse_pos[1] <= self.player_y_dict[scene] - 60:
                    text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render("+20% sát thương", True, pygame.Color(0, 0, 0))
                    wd.blit(text_surface, (5, self.player_y_dict[scene] - 95))
                elif 80 <= mouse_pos[0] <= 100 and self.player_y_dict[scene] - 80 <= mouse_pos[1] <= self.player_y_dict[scene] - 60:
                    text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render("+20% độc", True, pygame.Color(0, 0, 0))
                    wd.blit(text_surface, (26, self.player_y_dict[scene] - 95))
        
        if not self.players[1].dead() and self.players[1] in scene.players:
            if self.turn == 1:
                pygame.draw.rect(wd, pygame.Color(0, 0, 255), pygame.Rect(700, self.player_y_dict[scene], 100, 100))
            else:
                pygame.draw.rect(wd, pygame.Color(255, 0, 0), pygame.Rect(700, self.player_y_dict[scene], 100, 100))
            
            pygame.draw.rect(wd, pygame.Color(255, 127, 127), pygame.Rect(700, self.player_y_dict[scene] - 60, 100, 40))
            pygame.draw.rect(wd, pygame.Color(46, 204, 113), pygame.Rect(700, self.player_y_dict[scene] - 60, self.players[0].hp*100//self.players[0].max_hp, 20))
            pygame.draw.rect(wd, pygame.Color(0, 100, 0), pygame.Rect(700, self.player_y_dict[scene] - 40, min(self.players[0].poisoned_damage, self.players[0].max_hp)*100//self.players[0].max_hp, 20))
            if 700 <= mouse_pos[0] <= 800 and self.player_y_dict[scene] <= mouse_pos[1] <= self.player_y_dict[scene] + 100:
                pygame.draw.rect(wd, pygame.Color(128, 128, 128), pygame.Rect(600, self.player_y_dict[scene], 100, 200))
                text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render(f"HP: {integer_to_text(self.players[1].hp)}/{integer_to_text(self.players[1].max_hp)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (605, self.player_y_dict[scene] + 5))

                text_surface = pygame.font.SysFont("Consolas", 10, True).render(f"Công: {integer_to_text(self.players[1].damage)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (605, self.player_y_dict[scene] + 20))

                text_surface = pygame.font.SysFont("Consolas", 10, True).render(f"Độc: {integer_to_text(self.players[1].poison_damage)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (605, self.player_y_dict[scene] + 35))

                text_surface = pygame.font.SysFont("Consolas", 10, True).render(f"Hồi: {integer_to_text(self.players[1].heal_amount)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (605, self.player_y_dict[scene] + 50))

                text_surface = pygame.font.SysFont("Consolas", 10, True).render(f"Bị độc: {integer_to_text(self.players[1].poisoned_damage)}", True, pygame.Color(0, 0, 0))
                wd.blit(text_surface, (605, self.player_y_dict[scene] + 65))
            
            if self.turn == 0 and self.players[0].at is self.players[1].at:
                pygame.draw.rect(wd, pygame.Color(255, 60, 60), pygame.Rect(700, self.player_y_dict[scene] - 80, 20, 20))
                pygame.draw.rect(wd, pygame.Color(0, 100, 0), pygame.Rect(780, self.player_y_dict[scene] - 80, 20, 20))
                if 700 <= mouse_pos[0] <= 720 and self.player_y_dict[scene] - 80 <= mouse_pos[1] <= self.player_y_dict[scene] - 60:
                    text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render("Tấn công", True, pygame.Color(0, 0, 0))
                    wd.blit(text_surface, (726, self.player_y_dict[scene] - 75))
                elif 780 <= mouse_pos[0] <= 800 and self.player_y_dict[scene] - 80 <= mouse_pos[1] <= self.player_y_dict[scene] - 60:
                    text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render("Đầu độc", True, pygame.Color(0, 0, 0))
                    wd.blit(text_surface, (729, self.player_y_dict[scene] - 75))
            
            if self.turn == 1 and self.players[1].at.tower_owner is self.players[1]:
                pygame.draw.rect(wd, pygame.Color(255, 60, 60), pygame.Rect(700, self.player_y_dict[scene] - 80, 20, 20))
                pygame.draw.rect(wd, pygame.Color(0, 100, 0), pygame.Rect(780, self.player_y_dict[scene] - 80, 20, 20))

                if 700 <= mouse_pos[0] <= 720 and self.player_y_dict[scene] - 80 <= mouse_pos[1] <= self.player_y_dict[scene] - 60:
                    text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render("+20% sát thương", True, pygame.Color(0, 0, 0))
                    wd.blit(text_surface, (705, self.player_y_dict[scene] - 95))
                elif 780 <= mouse_pos[0] <= 800 and self.player_y_dict[scene] - 80 <= mouse_pos[1] <= self.player_y_dict[scene] - 60:
                    text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render("+20% độc", True, pygame.Color(0, 0, 0))
                    wd.blit(text_surface, (726, self.player_y_dict[scene] - 95))

        if self.players[self.turn].at.next is scene:
            pygame.draw.rect(wd, pygame.Color(128, 128, 128), pygame.Rect(350, 50, 100, 100))
            if 350 <= mouse_pos[0] <= 450 and 50 <= mouse_pos[1] <= 150:
                text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render(f"Đi {'tới' if self.turn == 0 else 'về'} {scene.name}", True, pygame.Color(0, 0, 0))
                surface_x: int = text_surface.get_size()[0]
                wd.blit(text_surface, (400 - surface_x // 2, 35))
        elif self.players[self.turn].at.previous is scene:
            pygame.draw.rect(wd, pygame.Color(128, 128, 128), pygame.Rect(350, 50, 100, 100))
            text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 10, True).render(f"Đi {'tới' if self.turn == 1 else 'về'} {scene.name}", True, pygame.Color(0, 0, 0))
            surface_x: int = text_surface.get_size()[0]
            wd.blit(text_surface, (400 - surface_x // 2, 35))

        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 32, True).render(scene.name, True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))