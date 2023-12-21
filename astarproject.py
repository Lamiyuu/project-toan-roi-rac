from typing import Optional

import pygame
import sys
import heapq
import time
from math import sqrt


# ALGORITHM: A* (A star) -----
# Define A* heuristic function
def heuristic(a, b) -> float:
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


# Define A* path finding function
def astar(grid, start, goal, grid_info, screen, finding_color) -> Optional[list]:
    # Get grid information
    grid_width = grid_info[0]
    grid_height = grid_info[1]
    grid_size = grid_info[2]

    # Implementation of A* algorithm here
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1),
                 (-1, 1)]  # Các vị trí có thể di chuyển lên xuống trái phải

    close_set = set()  # Danh sách đóng không cần xét lại
    came_from = {}  # Từ điển chứa tất cả các tuyến đường đã xét rồi tìm chỗ ngắn nhất
    gscore = {start: 0}  # Chi phí di chuyển từ điểm xuất phát đến điểm hiện tại
    fscore = {start: heuristic(start, goal)}  # f = g + h

    oheap = []  # Danh sách mở chứa vị trí đang được xét
    heapq.heappush(oheap, (fscore[start], start))  # Đưa vị trí xuất phát vào danh sách mở
    current_temp = start

    while oheap:
        current = heapq.heappop(oheap)[1]  # Vị trí có F nhỏ nhất
        current_temp = current
        # Khi đạt được mục tiêu trả về đường đi ngắn nhất
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data.reverse()
            return data

        close_set.add(current)  # Thêm current vào danh sách đóng
        for i, j in neighbors:  # Xét tất cả hàng xóm và tính G
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < grid_width:  # Bỏ qua các vị trí nằm ngoài lưới đc đi
                if 0 <= neighbor[1] < grid_height:
                    if grid[neighbor[1]][neighbor[0]] == 1:
                        continue
                else:
                    # Tường y
                    continue
            else:
                # Tường x
                continue
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue  # Bỏ qua trong tập đóng và điểm G lớn hơn hoặc bằng
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current

                gscore[neighbor] = tentative_g_score

                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                heapq.heappush(oheap, (fscore[neighbor], neighbor))
                pygame.draw.rect(screen, finding_color,
                                 [current_temp[0] * grid_size, current_temp[1] * grid_size, grid_size, grid_size])
                pygame.display.update()
                time.sleep(0.02)
    return None
