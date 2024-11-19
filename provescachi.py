#!/usr/bin/env python3

import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
pygame.init()
clock = pygame.time.Clock()
rule = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

# Define the window
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Roulette Game')
mouse = {'x': -1, 'y': -1}

# Spinning parameters for the roulette
angle = 265  # orientation so that 0 is at the top
girant = False
speed = 50
voltes = 0
buttons = [
    {'name': 'girar', 'x': 500, 'y': 400, 'width': 50, 'height': 50, 'pressed': False}
]

# Betting table grid configuration
button_start_x = 100  # Starting x position for betting buttons
button_start_y = 450  # Starting y position for betting buttons
button_width = 50
button_height = 50

# List of red and black numbers (based on a typical roulette layout)
rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Define the grid layout of the roulette betting table
betting_table = [
    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
    [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
]

# Function to create betting buttons
def create_betting_buttons():
    buttons = []
    y = button_start_y
    
    for row in betting_table:
        x = button_start_x
        for number in row:
            # Define button color based on red or black number
            if number == 0:
                color = GREEN  # 0 is green
            elif number in rojos:
                color = RED  # Number is in the red list
            elif number in negros:
                color = BLACK  # Number is in the black list
            
            # Create the button and add it to the list
            button = {
                'number': number,
                'rect': pygame.Rect(x, y, button_width, button_height),
                'color': color
            }
            buttons.append(button)
            x += button_width  # Move x to the right for the next button
        y += button_height  # Move y down for the next row
    
    return buttons

# Initialize betting buttons
betting_buttons = create_betting_buttons()

# Define custom buttons for PAR, RED, BLACK, IMP
custom_buttons = [
    {'label': 'PAR', 'x': button_start_x + button_width * 0, 'y': button_start_y + button_height * 4, 'width': button_width, 'height': button_height, 'color': WHITE, 'text_color': BLACK},
    {'label': 'RED', 'x': button_start_x + button_width * 3, 'y': button_start_y + button_height * 4, 'width': button_width, 'height': button_height, 'color': RED},
    {'label': 'BLACK', 'x': button_start_x + button_width * 6, 'y': button_start_y + button_height * 4, 'width': button_width, 'height': button_height, 'color': BLACK,'text_color':WHITE},
    {'label': 'IMP', 'x': button_start_x + button_width * 9, 'y': button_start_y + button_height * 4, 'width': button_width, 'height': button_height, 'color': WHITE, 'text_color': BLACK}
]

# Main application loop
def main():
    is_looping = True

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60)  # Limit to 60 FPS

    # Exit application
    pygame.quit()
    sys.exit()

# Handle events
def app_events():
    global mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEMOTION:
            mouse['x'], mouse['y'] = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if utils.is_point_in_rect(mouse, buttons[0]):
                girar_ruleta()
            
            # Check if any betting button was clicked
            for button in betting_buttons:
                if button['rect'].collidepoint(event.pos):
                    print(f"Button {button['number']} clicked!")  # Replace this with any desired action

            # Check if any custom button was clicked
            for custom_button in custom_buttons:
                rect = pygame.Rect(custom_button['x'], custom_button['y'], custom_button['width'], custom_button['height'])
                if rect.collidepoint(event.pos):
                    print(f"Custom Button {custom_button.get('label', 'RED/BLACK')} clicked!")  # Handle custom button click here
    return True

# Run calculations
def app_run():
    # To make the wheel spin
    global girant, speed, voltes, angle
    max_voltes = random.randint(0, 36)
    if girant:  # While spinning, add speed and rotations
        angle += speed
        if angle > 360:
            angle -= 360
            voltes += 1
        if voltes >= max_voltes:  # If it exceeds the max, slow down
            speed -= 1
        if speed <= 0:
            girant = False
            speed = 0

# Draw custom betting buttons on the screen
def draw_custom_buttons():
    for button in custom_buttons:
        rect = pygame.Rect(button['x'], button['y'], button['width'], button['height'])
        
        # Draw the button with its color
        pygame.draw.rect(screen, button['color'], rect)
        
        # Draw the white border around the button (thickness 1)
        pygame.draw.rect(screen, WHITE, rect, 1)  # The last argument is the thickness
        
        if 'label' in button and button['label']:  # Only draw label if it exists
            font = pygame.font.SysFont("Arial", 15)
            text_color = button.get('text_color', BLACK)
            label = font.render(button['label'], True, text_color)
            screen.blit(label, (rect.x + (button_width - label.get_width()) / 2, rect.y + (button_height - label.get_height()) / 2))

# Draw betting buttons on the screen
def draw_betting_buttons():
    for button in betting_buttons:
        pygame.draw.rect(screen, button['color'], button['rect'])
        
        # Draw the white border around the button (thickness 1)
        pygame.draw.rect(screen, WHITE, button['rect'], 1)  # The last argument is the thickness
        
        font = pygame.font.SysFont("Arial", 15)
        label = font.render(str(button['number']), True, WHITE if button['color'] == BLACK else BLACK)
        screen.blit(label, (button['rect'].x + (button_width - label.get_width()) / 2, 
                            button['rect'].y + (button_height - label.get_height()) / 2))

# Draw the app screen
def app_draw():
    # Fill background with white
    screen.fill(WHITE)

    # Draw the grid
    utils.draw_grid(pygame, screen, 50)
    
    # Draw betting buttons
    draw_betting_buttons()
    
    # Draw custom buttons
    draw_custom_buttons()
    
    # Draw the roulette wheel
    center = {"x": 300, "y": 250}
    for i, casella in enumerate(rule): 
        inici_angle = (360 / 37) * i + angle  # starting angle to draw segment
        fi_angle = (360 / 37) * (i + 1) + angle  # ending angle

        # Points for larger circle
        p0 = utils.point_on_circle(center, 100, inici_angle)
        p1 = utils.point_on_circle(center, 150, inici_angle)
        p2 = utils.point_on_circle(center, 150, fi_angle)
        p3 = utils.point_on_circle(center, 100, fi_angle)

       

        # Colors for roulette
        color = GREEN if i == 0 else RED if i % 2 == 1 else BLACK

        # Coordinates for drawing
        points = [
            (int(p0["x"]), int(p0["y"])),
            (int(p1["x"]), int(p1["y"])),
            (int(p2["x"]), int(p2["y"])),
            (int(p3["x"]), int(p3["y"]))
        ]

        
        coords = [  # Arrow pointing at the top
            (290, 90),
            (310, 90),
            (300, 115)
        ]

        # Draw polygons and numbers on the wheel
        pygame.draw.polygon(screen, color, points)
        
        # Place the number in the center of each roulette segment
        centre_quesito = utils.point_on_circle(center, 140, (inici_angle + fi_angle) / 2)
        fontnum = pygame.font.SysFont("Arial", 15)
        color_num = WHITE if color == BLACK else BLACK
        txt = fontnum.render(str(casella), True, color_num)

        # Draw the "Girar" button outline
        pygame.draw.rect(screen, BLACK, (buttons[0]["x"], buttons[0]["y"], buttons[0]["width"], buttons[0]["height"]), 5)
        
        # Place the number label on the segment
        screen.blit(txt, (int(centre_quesito["x"] - txt.get_width() / 2), int(centre_quesito["y"] - txt.get_height() / 2)))

    # Draw the main circle of the roulette
    pygame.draw.circle(screen, WHITE, (300, 250), 100, 5)
    # Draw the arrow at the top
    pygame.draw.polygon(screen, (255, 255, 0), coords, 3)
    pygame.draw.circle(screen, BLUE, (300, 90), 5, 5)

    # Update the display
    pygame.display.update()

# Reset values to start spinning the roulette
def girar_ruleta():
    global girant, speed, voltes, angle 
    girant = True
    speed = 50
    voltes = 0
    angle = 0

if __name__ == "__main__":
    main()

