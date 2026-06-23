import pygame
from sprites.textbox import TextBox
from game.game import Game
from game.place import Place
from typing import Tuple

pygame.init()

wd: pygame.Surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Tiến lên Miền Nam 2", "TLMN2")
clock: pygame.time.Clock = pygame.time.Clock()

running: bool = True
event_number: int = 0
p1_textbox: TextBox = TextBox(36, 16, 290, 26, pygame.Color(255, 0, 0), pygame.Color(0, 0, 0), "Consolas", 16, 30)
p2_textbox: TextBox = TextBox(36, 47, 290, 26, pygame.Color(0, 0, 255), pygame.Color(0, 0, 0), "Consolas", 16, 30)
finished_running: bool = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if event_number <= 1 or 3 <= event_number <= 10:
                    event_number += 1
                elif event_number == 2 and p1_textbox.text != "" and p2_textbox.text != "":
                    event_number += 1
            elif event_number == 2:
                p1_textbox.handle_event(event)
                p2_textbox.handle_event(event)
            elif event_number == 11:
                if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and not current_game.players[current_game.turn].dead() and current_scene.next is not None:
                    current_scene = current_scene.next
                
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and not current_game.players[current_game.turn].dead() and current_scene.previous is not None:
                    current_scene = current_scene.previous
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event_number == 2:
                p1_textbox.handle_event(event)
                p2_textbox.handle_event(event)
            elif event_number == 11:
                mouse: Tuple[int, int] = pygame.mouse.get_pos()
                if current_game.players[current_game.turn].dead():
                    finished_running = True
                elif (current_scene is current_game.players[current_game.turn].at.next or current_scene is current_game.players[current_game.turn].at.previous) and 350 <= mouse[0] <= 450 and 50 <= mouse[1] <= 150:
                    current_game.players[current_game.turn].at.players.remove(current_game.players[current_game.turn])
                    current_game.players[current_game.turn].at = current_scene
                    current_scene.players += [current_game.players[current_game.turn]]
                    finished_running = True
                elif not current_game.players[1-current_game.turn].dead() and current_game.players[1-current_game.turn].at_home_tower >= 10 and current_scene is current_game.players[current_game.turn].at and 350 <= mouse[0] <= 450 and 50 <= mouse[1] <= 150:
                    current_game.players[1-current_game.turn].hp //= 2
                    current_game.players[1-current_game.turn].at.hp //= 2
                    death_place: Place = current_game.players[1-current_game.turn].at
                    if current_game.players[1-current_game.turn].dead():
                        current_game.players[1-current_game.turn].death_trigger(f"{current_game.players[1-current_game.turn].name} đã bị quả bom của {current_game.players[current_game.turn].name} hủy diệt ở {death_place.name}")
                    
                    if death_place.dead():
                        death_place.switch_tower_owner(current_game.players[current_game.turn])
                    
                    finished_running = True
                elif current_scene is current_game.players[1-current_game.turn].at and not current_game.players[1-current_game.turn].dead():
                    if current_game.turn == 0:
                        if 700 <= mouse[0] <= 720 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[0].attack(current_game.players[1])
                            finished_running = True
                        elif 780 <= mouse[0] <= 800 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[1].poisoned_damage += current_game.players[0].poison_damage
                            finished_running = True
                    else:
                        if 0 <= mouse[0] <= 20 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[1].attack(current_game.players[0])
                            finished_running = True
                        elif 80 <= mouse[0] <= 100 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[0].poisoned_damage += current_game.players[1].poison_damage
                            finished_running = True
                elif current_scene.tower_owner == current_game.players[current_game.turn]:
                    if current_game.turn == 0:
                        if 0 <= mouse[0] <= 20 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[0].damage = int(current_game.players[0].damage * 1.2)
                            finished_running = True
                        elif 30 <= mouse[0] <= 50 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[0].hp = int(current_game.players[0].hp * 1.1)
                            current_game.players[0].max_hp = int(current_game.players[0].max_hp * 1.1)
                            finished_running = True
                        elif 50 <= mouse[0] <= 70 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[0].heal_amount = int(current_game.players[0].heal_amount * 1.5)
                            finished_running = True
                        elif 80 <= mouse[0] <= 100 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[0].poison_damage = int(current_game.players[0].poison_damage * 1.2)
                            finished_running = True
                        elif 0 <= mouse[0] <= 100 and current_game.player_y_dict[current_scene] - 100 <= mouse[1] <= current_game.player_y_dict[current_scene] - 80:
                            current_game.players[0].hp = min(current_game.players[0].hp + current_game.players[0].heal_amount, current_game.players[0].max_hp)
                            finished_running = True
                    else:
                        if 700 <= mouse[0] <= 720 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[1].damage = int(current_game.players[1].damage * 1.2)
                            finished_running = True
                        elif 730 <= mouse[0] <= 750 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[1].hp = int(current_game.players[1].hp * 1.1)
                            current_game.players[1].max_hp = int(current_game.players[1].max_hp * 1.1)
                            finished_running = True
                        elif 750 <= mouse[0] <= 770 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[1].heal_amount = int(current_game.players[1].heal_amount * 1.5)
                            finished_running = True
                        elif 780 <= mouse[0] <= 800 and current_game.player_y_dict[current_scene] - 80 <= mouse[1] <= current_game.player_y_dict[current_scene] - 60:
                            current_game.players[1].poison_damage = int(current_game.players[1].poison_damage * 1.2)
                            finished_running = True
                        elif 700 <= mouse[0] <= 800 and current_game.player_y_dict[current_scene] - 100 <= mouse[1] <= current_game.player_y_dict[current_scene] - 80:
                            current_game.players[1].hp = min(current_game.players[1].hp + current_game.players[1].heal_amount, current_game.players[1].max_hp)
                            finished_running = True
        elif event.type == pygame.TEXTINPUT:
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
        current_game: Game = Game(p1_textbox.text, p2_textbox.text)
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
        pygame.draw.rect(wd, pygame.Color(153, 0, 76), pygame.Rect(500, 50, 100, 100))
        pygame.draw.rect(wd, pygame.Color(102, 0, 51), pygame.Rect(650, 50, 100, 100))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Hà Nội", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (73, 92))
        
        text_surface = pygame.font.SysFont("Consolas", 16).render("Thanh Hóa", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (209, 92))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Huế", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (386, 92))
        
        text_surface = pygame.font.SysFont("Consolas", 16).render("Đắk Lắk", True, pygame.Color(255, 255, 255))
        wd.blit(text_surface, (518, 92))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Sài Gòn", True, pygame.Color(255, 255, 255))
        wd.blit(text_surface, (668, 92))

        pygame.draw.rect(wd, pygame.Color(155, 118, 83), pygame.Rect(150, 90, 50, 20))
        pygame.draw.rect(wd, pygame.Color(155, 118, 83), pygame.Rect(300, 90, 50, 20))
        pygame.draw.rect(wd, pygame.Color(155, 118, 83), pygame.Rect(450, 90, 50, 20))
        pygame.draw.rect(wd, pygame.Color(155, 118, 83), pygame.Rect(600, 90, 50, 20))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Mỗi địa điểm trên bản đồ có 1 cái tháp:", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 160))
        
        text_surface = pygame.font.SysFont("Consolas", 16).render(f"- Tháp của Hà Nội và Thanh Hóa là của {p1_textbox.text}", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (10, 176))

        text_surface = pygame.font.SysFont("Consolas", 16).render(f"- Tháp của Đắk Lắk và Sài Gòn là của {p2_textbox.text}", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (10, 192))

        text_surface = pygame.font.SysFont("Consolas", 16).render("- Tháp của Huế chưa là của ai", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (10, 208))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 224))
    elif event_number == 5:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Có 3 trường hợp có thể xảy ra:", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render("1. Bạn đang ở địa điểm có tháp của bạn", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (10, 16))

        text_surface = pygame.font.SysFont("Consolas", 16).render("2. Bạn đang ở địa điểm có tháp của đối thủ", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (10, 32))

        text_surface = pygame.font.SysFont("Consolas", 16).render("3. Bạn đang ở địa điểm có tháp không có người sở hữu", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (10, 48))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 64))
    elif event_number == 6:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Nếu bạn đang ở địa điểm có tháp của bạn, thì bạn có thể hồi máu và nâng cấp các thuộc", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render("tính của bạn", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 16))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 32))
    elif event_number == 7:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Nếu bạn đang ở địa điểm có tháp của đối thủ, thì bạn sẽ bị mất máu, không thể hồi máu và", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render("nâng cấp các thuộc tính của bạn", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 16))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 32))
    elif event_number == 8:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Nếu bạn đang ở địa điểm có tháp không có chủ sở hữu, thì bạn sẽ không thể hồi máu và nâng", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render("cấp các thuộc tính của bạn nhưng cũng không mất máu", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 16))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 32))
    elif event_number == 9:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render(f"Nhiệm vụ của {p1_textbox.text} là chiếm tháp của Sài Gòn", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render(f"Còn nhiệm vụ của {p2_textbox.text} là chiếm tháp của Hà Nội", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 16))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 32))
    elif event_number == 10:
        text_surface: pygame.Surface = pygame.font.SysFont("Consolas", 16).render("Chúc may mắn...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 0))

        text_surface = pygame.font.SysFont("Consolas", 16).render("Nhấn enter để tiếp tục...", True, pygame.Color(0, 0, 0))
        wd.blit(text_surface, (0, 16))
    else:
        if finished_running:
            current_game.before_turn()
            current_game.after_turn()
            finished_running = False
            current_scene: Place = current_game.players[current_game.turn].at

        current_game.render_scene(wd, current_scene)

    pygame.display.flip()