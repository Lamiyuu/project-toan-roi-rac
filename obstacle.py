from PIL import Image
import numpy as np
def get_obstacle(image_path):
    image = Image.open(image_path)
    image = image.resize((600,600))
    
    #Chia ra các ô grid
    global grid_height, grid_width
    grid_width = 20
    grid_height = 20

    num_rows = image.size[0] // grid_height
    num_cols = image.size[1] // grid_width

    obstacle_coordinates = []
    # Xác định ngưỡng để phân biệt giữa màu đen và màu trung bình của ô grid
    threshold_value = 220  # Giá trị ngưỡng (có thể điều chỉnh)

    for row in range(num_rows):
        for col in range(num_cols):
            top = row * grid_height
            bottom = (row + 1) * grid_height
            left = col * grid_width
            right = (col + 1) * grid_width
            grid_image = image.crop((left, top, right, bottom))
            grid_array = np.array(grid_image)
            average_color = np.mean(grid_array)
            if average_color < threshold_value:
                obstacle_coordinates.append((col, row))
                

    return obstacle_coordinates