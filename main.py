import pygame, sys
from pygame.locals import*
import time
from PIL import Image
import pygame_gui
from bfsproject import bfs
from astarproject import astar
# algorithm mapping
algorithm_mapping = {
    'BFS' : 'bfs',
    'A*'  : 'astar'
}
# Map user-friendly names to map identifiers
'''
map_mapping = {
    'Map 1': 'map1',
    'Map 2': 'map2',
    'Map 3': 'map3',
}
'''
#2 màu cơ bản thiết kế giao diện 
color1 = (0, 112, 192) # màu xanh 

color2 = (233, 143, 23) # màu cam 

white = (255, 255, 255)

red = (255, 0, 0)

black = (0, 0, 0)

yellow = (255, 255, 0)

green = (0, 255, 0)

blue = (0, 0, 255)
#Các ảnh sử dụng làm điểm đầu và điểm cuối
'''
imgae_start_point = pygame.image.load("images/agent1.png")

image_end_point = pygame.image.load("images/flag.png")
'''
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
def setup_grid(grid, limit_rect):
    for y in range(limit_rect.top, limit_rect.bottom):
        for x in range(limit_rect.left, limit_rect.right):
            grid[y][x] = 0
#Start point 
def draw_start_point(screen, start_point, grid_size, color)->None:
    if start_point:
        pygame.draw.polygon(screen,
                            color,
                            [(start_point[0] * grid_size + grid_size // 2, start_point[1] * grid_size),
                            (start_point[0] * grid_size,
                            start_point[1] * grid_size + grid_size),
                            (start_point[0] * grid_size + grid_size,
                            start_point[1] * grid_size + grid_size)])

#End point
def draw_end_point(screen, end_point, grid_size, color)->None:
    if end_point:
        pygame.draw.circle(screen,
                          color,
                          (end_point[0] * grid_size + grid_size // 2,
                          end_point[1] * grid_size + grid_size // 2),
                          grid_size // 2)
# Define draw obstacles function
def draw_obstacles(screen, obstacles, grid_size, color)->None:
    for obstacle in obstacles:
        pygame.draw.rect(screen, black, (obstacle[0] * grid_size, obstacle[1] * grid_size, grid_size, grid_size))
        
# Define draw route function
def draw_route(screen, route, grid_size, color, find_way)-> None:
    # If route is None, print "Khong tim duoc duong di"   
    if route is None:
        print("Khong tim duoc duong di")
    elif find_way:
        for pos in route:
            pygame.draw.rect(screen, color, [pos[0] * grid_size, pos[1] * grid_size, grid_size, grid_size])
#Trả về ảnh 400*400
'''
def image_processing(image_path):
    image = Image.open(image_path)
    image = image.resize((600,600))
    return image
'''
# MAIN PROGRAM ----- 
# main function

def main() -> None:
    # Initialize pygame
    pygame.init()

    #window size
    window_size = (900, 650)
    # Set window dimensions and creat window
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Project toan roi rac nhom 3")

    #create gui manager
    gui_manager = pygame_gui.UIManager(window_size)

    #Cho toàn màn hình màu trắng
    screen.fill(white)

    #Hiển thị vùng phía trên màu xanh dương hình chữ nhật 
    rect1 = pygame.Rect(0, 0, 900, 50)
    pygame.draw.rect(screen, color1, rect1)

    #Hiển thị bên phải hình chữ nhật màu cam:
    rect2 = pygame.Rect(600, 50, 300, 600)
    pygame.draw.rect(screen, color2, rect2)

    #create dropmenu select algorithm
    algorithm_choices = list(algorithm_mapping.keys())
    algorithm_selector = pygame_gui.elements.UIDropDownMenu(options_list= ['Select Algorithm', ''] + algorithm_choices,
                                                            starting_option=algorithm_choices[0],
                                                            relative_rect = pygame.Rect(650, 100, 200, 30), 
                                                            manager= gui_manager)

    '''    
    #create map dropmenu 
    # Create map dropdown menu
    #map_choices = list(map_mapping.keys())
    #map_selector = pygame_gui.elements.UIDropDownMenu(options_list=[('Select Map', '')] + map_choices,
                                                  #starting_option=map_choices[0],
                                                  #relative_rect=pygame.Rect(650, 200, 200, 30),
                                                  #manager=gui_manager)
    '''

    # FPS
    FPS = 60
    fpsClock = pygame.time.Clock()
    # Trong hàm main, sau khi tạo grid:
    grid = [[0 for _ in range(window_size[0]// 20)] for _ in range(window_size[1] // 20)]

    # Khoảng giới hạn là ô 600x600 từ (0, 50) đến (600, 650)
    limit_rect = pygame.Rect(0, 50, 600, 600)
    setup_grid(grid, limit_rect)

    # Create a button to start pathfinding
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(650, 500, 150, 30),
        text='Start',
        manager=gui_manager
    )
    # Obstacles, start point, end point
    obstacles = []
    start_point = None
    end_point = None
    
    running = True
    find_way = False
    route = []
    done = False
    selected_algorithm = None

    # When running is True, the main loop runs
    while running:
        time_delta = fpsClock.tick(FPS) / 1000.0
        #Event handling
        for event in pygame.event.get():
            #Quit pygame
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x , grid_y = round(x/20) , round( y/ 20)
                #Kiểm tra tọa độ 
                if limit_rect.collidepoint(x, y):
                    if event.button == 1:
                        # Left mouse button: Set start and end points, add obstacles
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

                    elif event.button == 3:
                        # Right mouse button: Remove obstacles
                        if (grid_x, grid_y) in obstacles:
                            obstacles.remove((grid_x, grid_y))
                            grid[grid_y][grid_x] = 0
                            find_way = False
                            route = [] 
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == algorithm_selector:
                        selected_algorithm = event.text

                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == start_button and selected_algorithm:
                            if selected_algorithm == "A*":
                                route = astar(grid, start_point, end_point, [30, 30, 20], screen, yellow)
                                find_way = True
                                done = True
                            else :
                                route = bfs(grid, start_point, end_point, [30, 30, 20], screen, yellow)
                                find_way = True
                                done = True
        draw_grid(screen, window_size, black, 20, limit_rect)

        draw_start_point(screen, start_point, 20, red)

        draw_end_point(screen, end_point, 20, blue)

        if find_way and route:
            draw_route(screen, route, 20, green, find_way)
        if obstacles:
            draw_obstacles(screen, obstacles, 20, black)

        # Cập nhật GUI manager
        gui_manager.update(time_delta)

        # Vẽ GUI
        gui_manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()