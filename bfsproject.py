from typing import Optional
from collections import deque


def bfs(grid, start, goal, grid_info, screen) -> Optional[tuple]:
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
    considered_neighbors = []
    while queue:
        current = queue.popleft()
        current = current
        if current == goal:
            # Đã tìm được đường đi 
            path = []
            while current != start:
                path.insert(0, current)
                current = parent[current]
            path.insert(0, start)
            return path, considered_neighbors
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
                considered_neighbors.append(neighbor)
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return None, considered_neighbors    