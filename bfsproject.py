from typing import Optional

import pygame
import sys
from collections import deque
import time
def bfs(grid, start, goal, grid_info, screen, finding_color) -> Optional[list]:
    # Get grid information
    grid_width = grid_info[0]
    grid_height = grid_info[1]
    grid_size = grid_info[2]
    
    # Implementation of A* algorithm here
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Các vị trí có thể di chuyển lên xuống trái phải
    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    parent = {}
    while queue:
        current = queue.popleft()

        if current == goal:
            # Đã tìm được đường đi 
            path = []
            while current != start:
                path.insert(0, current)
                current = parent[current]
            path.insert(0, start)
            return path
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            if 0 <= neighbor[0] < grid_width:       #Bỏ qua các vị trí nằm ngoài lưới đc đi
                if 0 <= neighbor[1] < grid_height:                
                    if grid[neighbor[1]][neighbor[0]] == 1:
                        continue
                else: 
                    # Tường y
                    continue    
            else:
                # Tường x
                continue
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current
                pygame.draw.rect(screen, finding_color, [current[0] * grid_size, current[1] * grid_size, grid_size, grid_size])
                pygame.display.update()
                time.sleep(0.02) 
    return None    