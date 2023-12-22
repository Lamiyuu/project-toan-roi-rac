import pygame as pg

def draw_dropdown(surf, rect, color_menu, color_option, font, main, options, draw_menu, active_option):
    pg.draw.rect(surf, color_menu[draw_menu], rect, 0)
    msg = font.render(main, 1, (0, 0, 0))
    surf.blit(msg, msg.get_rect(center=rect.center))

    if draw_menu:
        for i, text in enumerate(options):
            option_rect = rect.copy()
            option_rect.y += (i + 1) * rect.height
            pg.draw.rect(surf, color_option[1 if i == active_option else 0], option_rect, 0)
            msg = font.render(text, 1, (0, 0, 0))
            surf.blit(msg, msg.get_rect(center=option_rect.center))

def update_dropdown(rect, event_list, draw_menu, active_option):
    mpos = pg.mouse.get_pos()
    menu_active = rect.collidepoint(mpos)
    
    active_option = -1
    for i in range(len(options)):
        option_rect = rect.copy()
        option_rect.y += (i + 1) * rect.height
        if option_rect.collidepoint(mpos):
            active_option = i
            break

    if not menu_active and active_option == -1:
        draw_menu = False

    for event in event_list:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if menu_active:
                draw_menu = not draw_menu
            elif draw_menu and active_option >= 0:
                draw_menu = False
                return active_option, draw_menu
    return -1, draw_menu

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((640, 480))

COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

font = pg.font.SysFont(None, 30)

rect = pg.Rect(50, 50, 200, 50)
main_text = "Select Mode"
options = ["Calibration", "Test"]
draw_menu = False
active_option = -1

run = True
while run:
    clock.tick(30)

    event_list = pg.event.get()
    for event in event_list:
        if event.type == pg.QUIT:
            run = False

    selected_option, draw_menu = update_dropdown(rect, event_list, draw_menu, active_option)
    if selected_option >= 0:
        main_text = options[selected_option]
        

    screen.fill((255, 255, 255))
    draw_dropdown(screen, rect, [COLOR_INACTIVE, COLOR_ACTIVE], [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], font, main_text, options, draw_menu, active_option)
    pg.display.flip()
    
pg.quit()
exit()
