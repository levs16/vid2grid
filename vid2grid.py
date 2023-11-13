# Import pygame and other modules
import pygame
import sys
import cv2 # For video processing

# Initialize pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the size of the grid
GRID_SIZE = 80

# Define the size of the window
WINDOW_WIDTH = 1660
WINDOW_HEIGHT = 1024

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Video Grid")

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Ask the user for the video file name
video_file = input("Enter the video file name: ")

# Open the video file using cv2
video = cv2.VideoCapture(video_file)

# Check if the video file is valid
if not video.isOpened():
    print("Invalid video file")
    sys.exit()

# Get the video frame rate
fps = video.get(cv2.CAP_PROP_FPS)

# Get the video frame size
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calculate the size of each cell in the grid
cell_width = WINDOW_WIDTH // GRID_SIZE
cell_height = WINDOW_HEIGHT // GRID_SIZE

# Create a list to store the average color of each cell
cell_colors = []

# Loop until the user quits or the video ends
running = True
while running:
    # Get the next frame from the video
    ret, frame = video.read()

    # Check if the frame is valid
    if not ret:
        break

    # Convert the frame from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize the frame to fit the window
    frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Clear the cell colors list
    cell_colors.clear()

    # Loop through the grid rows
    for i in range(GRID_SIZE):
        # Loop through the grid columns
        for j in range(GRID_SIZE):
            # Get the coordinates of the top left corner of the cell
            x = j * cell_width
            y = i * cell_height

            # Get the sub-image of the cell from the frame
            cell = frame[y:y+cell_height, x:x+cell_width]

            # Calculate the average color of the cell
            cell_color = cell.mean(axis=0).mean(axis=0)

            # Append the cell color to the list
            cell_colors.append(cell_color)

    # Fill the screen with black
    screen.fill(BLACK)

    # Loop through the cell colors list
    for i, cell_color in enumerate(cell_colors):
        # Get the row and column index of the cell
        row = i // GRID_SIZE
        col = i % GRID_SIZE

        # Get the coordinates of the top left corner of the cell
        x = col * cell_width
        y = row * cell_height

        # Create a rectangle object for the cell
        cell_rect = pygame.Rect(x, y, cell_width, cell_height)

        # Draw the cell with the average color
        pygame.draw.rect(screen, cell_color, cell_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to match the video frame rate
    clock.tick(fps)

    # Handle the events
    for event in pygame.event.get():
        # If the user clicks the close button, quit the program
        if event.type == pygame.QUIT:
            running = False

# Release the video object
video.release()

# Quit pygame
pygame.quit()