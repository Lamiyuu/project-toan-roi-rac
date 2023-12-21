import pygame
import sys
def get_obstacle(image_data):
    # Assuming the image_data is a 2D list representing the color of each pixel
    image_width = len(image_data)
    image_height = len(image_data[0])

    # Create a Pygame surface from the image data
    cell_size = 20  # Adjust the cell size as needed
    image = pygame.Surface((image_width * cell_size, image_height * cell_size))

    for x in range(image_width):
        for y in range(image_height):
            # Calculate the position in the new surface
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)

            # Set the color of the cell based on the pixel color
            pixel_color = image_data[x][y]
            image.fill(pixel_color, rect)

    # List to store obstacle positions
    obstacles = []

    # Examine each cell in the image
    for x in range(image_width):
        for y in range(image_height):
            cell_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pixel_color = image.get_at(cell_rect.topleft)

            # Check if the cell is black (obstacle)
            if pixel_color == (0, 0, 0, 255):  # Assuming RGBA format, adjust if needed
                obstacles.append((x, y))

    return obstacles