import pygame, sys
from pygame.locals import *
import time
from PIL import Image
import sys
from bfsproject import bfs
from astarproject import astar
from dijkstraproject import dijktra
from obstacle import get_obstacle
options = ["BFS", "A*", "Dijktra"]
map_options = ["Map1", "Map2", "Map3"]
TOP_PAD = 50
RIGHT_PAD = 300

# 2 màu cơ bản thiết kế giao diện
color1 = (0, 112, 192)  # màu xanh

color2 = (233, 143, 23)  # màu cam

white = (255, 255, 255)

red = (255, 0, 0)

black = (0, 0, 0)

yellow = (255, 255, 0)

green = (0, 255, 0)

blue = (0, 0, 255)

COLOR_INACTIVE = (100, 80, 255)

COLOR_ACTIVE = (100, 200, 255)

COLOR_LIST_INACTIVE = (255, 100, 100)

COLOR_LIST_ACTIVE = (255, 150, 150)


# Ham khoi tao dropdown
def draw_dropdown(surf, rect, color_menu, color_option, font, main, option, draw_menu):
    pygame.draw.rect(surf, color_menu[draw_menu], rect, 0)
    msg = font.render(main, 1, (0, 0, 0))
    surf.blit(msg, msg.get_rect(center=rect.center))
    if draw_menu:
        for i, text in enumerate(option):
            option_rect = rect.copy()
            option_rect.y += (i + 1) * rect.height
            pygame.draw.rect(surf, color_option[0], option_rect, 0)
            msg = font.render(text, 1, (0, 0, 0))
            surf.blit(msg, msg.get_rect(center=option_rect.center))


def update_dropdown(rect, event_list, draw_menu):
    mpos = pygame.mouse.get_pos()
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu_active:
                draw_menu = not draw_menu
            elif draw_menu and active_option >= 0:
                draw_menu = False
                return active_option, draw_menu
    return -1, draw_menu


# Define function to draw grid function
def draw_grid(screen, window_infor, grid_color, grid_size, limit_rect=None) -> None:
    # Get window dimensions
    width = window_infor[0]
    height = window_infor[1]

    # Set the limit rect if provided
    limit_rect = limit_rect or pygame.Rect(0, 0, width, height)

    # Draw grid within the limit_rect
    for x in range(0, limit_rect.width, grid_size):
        x_pos = limit_rect.left + x
        if limit_rect.left <= x_pos < limit_rect.right:
            pygame.draw.line(screen, grid_color, (x_pos, limit_rect.top), (x_pos, limit_rect.bottom))

    for y in range(0, limit_rect.height, grid_size):
        y_pos = limit_rect.top + y
        if limit_rect.top <= y_pos < limit_rect.bottom:
            pygame.draw.line(screen, grid_color, (limit_rect.left, y_pos), (limit_rect.right, y_pos))


def setup_grid(limit_rect):
    return [[0 for _ in range(limit_rect.left, limit_rect.right)] for _ in range(limit_rect.top, limit_rect.bottom)]


# Start point
def draw_start_point(screen, start_point, grid_size, color) -> None:
    if start_point:
        pygame.draw.polygon(
            screen,
            color,
            [
                (start_point[0] * grid_size + grid_size // 2, TOP_PAD + start_point[1] * grid_size),
                (start_point[0] * grid_size, TOP_PAD + start_point[1] * grid_size + grid_size),
                (start_point[0] * grid_size + grid_size, TOP_PAD + start_point[1] * grid_size + grid_size)
            ])


# End point
def draw_end_point(screen, end_point, grid_size, color) -> None:
    if end_point:
        pygame.draw.circle(
            screen,
            color,
            (end_point[0] * grid_size + grid_size // 2, TOP_PAD + end_point[1] * grid_size + grid_size // 2),
            grid_size // 2
        )


# Define draw obstacles function
def draw_obstacles(screen, obstacles, grid_size, color) -> None:
    for obstacle in obstacles:
        pygame.draw.rect(
            screen,
            black,
            (
                obstacle[0] * grid_size,
                obstacle[1] * grid_size + TOP_PAD,
                grid_size,
                grid_size)
        )


# Define draw route function
def draw_route(screen, route, grid_size, color, find_way) -> None:
    # If route is None, print "Khong tim duoc duong di"   
    if route is None:
        print("Khong tim duoc duong di")
    elif find_way:
        for pos in route[1:-1]:
            pygame.draw.rect(screen, color, [pos[0] * grid_size, (pos[1] ) * grid_size + TOP_PAD, grid_size, grid_size])

#Defind draw considered_neighbor
def draw_considered_neighbor(screen, neighbor, grid_size, color, find_neighbor):
    if neighbor is None:
        print("Khong tim duoc duong di")
    elif find_neighbor:
        for pos in neighbor:
            pygame.draw.rect(screen, color, [pos[0] * grid_size, (pos[1] ) * grid_size + TOP_PAD, grid_size, grid_size])
            pygame.display.update()
            time.sleep(0.02)
# Trả về ảnh 600x600

def image_processing(screen ,image_path, position ):
    image = Image.open(image_path)
    image = image.resize((600, 600))

    # Chuyển đổi ảnh thành định dạng Pygame Surface
    pygame_surface = pygame.image.frombuffer(image.tobytes(), image.size, image.mode)

    # Vẽ ảnh lên màn hình Pygame
    screen.blit(pygame_surface, position)


# MAIN PROGRAM -----
# main function
#Các trạng thái:

def main() -> None:
    # Initialize pygame
    pygame.init()

    # window size
    window_size = (900, 650)
    # Set window dimensions and creat window
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Project toan roi rac nhom 3")

    # Cho toàn màn hình màu trắng
    screen.fill(white)

    #Hiển thị ảnh trên màn hình 
    map1 = "images/map1.png"
    map2 = "images/map2.png"
    map3 = "images/map3.png"
    # Hiển thị vùng phía trên màu xanh dương hình chữ nhật
    rect1 = pygame.Rect(0, 0, 900, TOP_PAD)


    # Hiển thị bên phải hình chữ nhật màu cam:
    rect2 = pygame.Rect(600, 50, RIGHT_PAD, 900)

    # Các biến của dropdown algorithm:
    font = pygame.font.SysFont(None, 20)
    rect = pygame.Rect(650, 100, 150, 50)
    main_text = "Select Algorithm"
    draw_menu = False
    #Các biến của của dropdown Map:
    font_map = pygame.font.SysFont(None, 20)
    rect_map = pygame.Rect(650, 400, 150, 50)
    main_text_map = "Select Map"
    draw_menu_map = False
    # FPS
    FPS = 60

    # Khoảng giới hạn là ô 600x600 từ (0, 50) đến (600, 650)
    limit_rect = pygame.Rect(0, TOP_PAD, 600, 600)
    grid = setup_grid(limit_rect)

    # Obstacles, start point, end point
    obstacles = []
    start_point = None
    end_point = None

    running = True
    find_way = False
    route = []
    neighbor = []
    done = False
    find_neighbor = False
    run_algorithm = False
    select_map = False

    #Biến lưu lại thời gian, chiều dài đường đi và ghi lên màn hình 
    total_path_length = 0
    font_info = pygame.font.Font(None, 30)
    start_time = 0
    end_time = 0

    # When running is True, the main loop runs
    while running:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, color1, rect1)
        pygame.draw.rect(screen, color2, rect2)
        # Event handling
        event_list = pygame.event.get()
        for event in event_list:
            # Quit pygame
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // 20, (y - TOP_PAD) // 20
                # Kiểm tra tọa độ
                if limit_rect.collidepoint(x, y):
                    if event.button == 1:
                        # Left mouse button: Set start and end xpoints, add obstacles
                        if (grid_x, grid_y) not in obstacles and not done:
                            if start_point is None:
                                start_point = (grid_x, grid_y)
                                grid[grid_y][grid_x] = 2

                            elif end_point is None:
                                end_point = (grid_x, grid_y)
                                grid[grid_y][grid_x] = 3

                            else:
                                obstacles.append((grid_x, grid_y))
                                grid[grid_y][grid_x] = 1
                                find_way = False
                                route = []
                                done = False
                                find_neighbor = False
                                select_map = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    find_neighbor = True
                    done = True
                    find_way = True
                    run_algorithm = True
                    select_map = True  # Bắt đầu chạy thuật toán khi nhấn phím Enter
                    start_time = time.time()
                if event.key == pygame.K_SPACE:
                    select_map = True
                    find_way = False
                    done = False
                    find_neighbor = False
                    run_algorithm = False
        selected_option, draw_menu = update_dropdown(rect, event_list, draw_menu)
        if selected_option >= 0:
            main_text = options[selected_option]
        
        selected_option_map, draw_menu_map = update_dropdown(rect_map, event_list, draw_menu_map)
        if selected_option_map >=0:
            main_text_map = map_options[selected_option_map]

        if select_map:
            if main_text_map == "Map1":
                image_processing(screen, map1, (0, TOP_PAD))
                obstacles = get_obstacle(map1)
                for pos in obstacles:
                    grid[pos[1]][pos[0]] = 1
            elif main_text_map == "Map2":
                image_processing(screen, map2, (0, TOP_PAD))
                obstacles = get_obstacle(map2)
                for pos in obstacles:
                    grid[pos[1]][pos[0]] = 1
            elif main_text_map == "Map3":
                image_processing(screen, map3, (0, TOP_PAD))
                obstacles = get_obstacle(map3)
                for pos in obstacles:
                    grid[pos[1]][pos[0]] = 1
        draw_grid(screen, window_size, black, 20, limit_rect)

        draw_start_point(screen, start_point, 20, red)

        draw_end_point(screen, end_point, 20, blue)

        draw_dropdown(screen, rect, [COLOR_INACTIVE, COLOR_ACTIVE], [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], font,
                      main_text, options, draw_menu)
        draw_dropdown(screen, rect_map, [COLOR_INACTIVE, COLOR_ACTIVE], [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], font_map,
                      main_text_map, map_options, draw_menu_map)
        #if obstacles:
            #draw_obstacles(screen, obstacles, 20, black)
        if run_algorithm:
            # Chạy thuật toán ở đây
            if main_text == "BFS":
                route, neighbor = bfs(grid, start_point , end_point, (30, 30, 20), screen)
                for i in range(len(route) - 1):
                    pos1 = route[i]
                    pos2 = route[i + 1]
                    total_path_length += ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5 * 20
            elif main_text == "A*":
                route, neighbor = astar(grid, start_point , end_point, (30, 30, 20), screen)
                for i in range(len(route) - 1):
                    pos1 = route[i]
                    pos2 = route[i + 1]
                    total_path_length += ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5 * 20
            elif main_text == "Dijktra":
                route, neighbor = dijktra(grid, start_point , end_point, (30, 30, 20), screen)
                for i in range(len(route) - 1):
                    pos1 = route[i]
                    pos2 = route[i + 1]
                    total_path_length += ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5 * 20
            run_algorithm = False  # Đặt lại để tránh chạy liên tục
            end_time = time.time()
        if find_neighbor and neighbor:
            draw_considered_neighbor(screen, neighbor, 20, yellow, find_neighbor)
            find_neighbor = False
        if find_way and route:
            draw_route(screen, route, 20, green, find_way)
        if end_time > start_time:
            running_time = end_time - start_time
            running_time_text = f"Running time: {running_time:.6f}s"
            running_time_surface = font_info.render(running_time_text, True, (0, 0, 0))
            screen.blit(running_time_surface, (0,20))
        if total_path_length > 0:
            path_length_text = f"Path length: {total_path_length:.6f}"
            path_length_surface = font_info.render(path_length_text, True, (0, 0, 0))
            screen.blit(path_length_surface,(400, 20))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
