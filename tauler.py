import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils
import random

mouse = {'x': -1, 'y': -1}
# Betting table grid configuration
button_start_x = 100  # Starting x position for betting buttons
button_start_y = 450  # Starting y position for betting buttons
button_width = 50
button_height = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# List of red and black numbers (based on a typical roulette layout)
rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Define the grid layout of the roulette betting table
betting_table = [
    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
    [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
]


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
                'x':x,
                'y':y,
                'height': button_height,
                'width': button_width,
                'color': color
            }
            buttons.append(button)
            x += button_width  # Move x to the right for the next button
        y += button_height  # Move y down for the next row
    
    return buttons


betting_buttons = create_betting_buttons()

# Define custom buttons for PAR, RED, BLACK, IMP
custom_buttons = [
    {'label': '0', 'x':50, 'y': 450, 'width': button_width, 'height': button_height * 3, 'color': GREEN, 'text_color': BLACK},
    {'label': 'PAR', 'x': button_start_x + button_width * 0, 'y': button_start_y + button_height * 3, 'width': button_width * 3, 'height': button_height, 'color': WHITE, 'text_color': BLACK},
    {'label': 'RED', 'x': button_start_x + button_width * 3, 'y': button_start_y + button_height * 3, 'width': button_width * 3, 'height': button_height, 'color': RED},
    {'label': 'BLACK', 'x': button_start_x + button_width * 6, 'y': button_start_y + button_height * 3, 'width': button_width* 3, 'height': button_height, 'color': BLACK,'text_color':WHITE},
    {'label': 'IMP', 'x': button_start_x + button_width * 9, 'y': button_start_y + button_height * 3, 'width': button_width* 3, 'height': button_height, 'color': WHITE, 'text_color': BLACK},
    {'label': '2 to 1', 'x': 700, 'y': 450, 'width': button_width, 'height': button_height, 'color': WHITE, 'text_color': BLACK},
    {'label': '2 to 1', 'x': 700 , 'y': 500, 'width': button_width, 'height': button_height, 'color': WHITE, 'text_color': BLACK},
    {'label': '2 to 1', 'x': 700,'y': 550, 'width': button_width, 'height': button_height, 'color': WHITE, 'text_color': BLACK},]

def draw_custom_buttons(screen):
    for button in custom_buttons:
        rect = pygame.Rect(button['x'], button['y'], button['width'], button['height'])
        
        # Dibujar el botón con su color
        pygame.draw.rect(screen, button['color'], rect)
        
        pygame.draw.rect(screen, WHITE, rect, 1)  
        
        if 'label' in button and button['label']:  
            font = pygame.font.SysFont("Arial", 15)
            if button['label'] == 'BLACK':
                color = WHITE
            else:
                color  = BLACK
            label = font.render(str(button['label']), True, color)
            # Calcular la posición para centrar el texto dentro del botón
            text_x = rect.x + (button['width'] - label.get_width()) / 2
            text_y = rect.y + (button['height'] - label.get_height()) / 2
            
            # Dibujar el texto centrado en el botón
            screen.blit(label, (text_x, text_y))


# Draw betting buttons on the screen
def draw_betting_buttons(screen):
    for button in betting_buttons:
        pygame.draw.rect(screen, button['color'], (button['x'],button['y'],button['width'],button['height']))
        
        # Draw the white border around the button (thickness 1)
        pygame.draw.rect(screen, WHITE, (button['x'],button['y'],button['width'],button['height']), 1)  # The last argument is the thickness
        
        font = pygame.font.SysFont("Arial", 15)
        label = font.render(str(button['number']), True, WHITE if button['color'] == BLACK else BLACK)
        screen.blit(label, (button['x'] + (button_width - label.get_width()) / 2, 
                            button['y'] + (button_height - label.get_height()) / 2))
