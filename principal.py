#!/usr/bin/env python3

import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils
import random

# Definir colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)  
GREEN = (0, 255, 0)
pygame.init()
clock = pygame.time.Clock()
rule = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27,13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
# Definir la finestra
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Window Title')
mouse = {'x':-1,'y':-1}

#GIROS RULETA

angle = 265 #orientacion pa que el 0 este pa arriba
girant = False
speed = 50
voltes = 0
buttons = [
    {'name': 'girar', 'x': 500, 'y': 400,'width':50,'height':50, 'pressed': False}
]

# Bucle de l'aplicació
def main():
    is_looping = True

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60) # Limitar a 60 FPS

    # Fora del bucle, tancar l'aplicació
    pygame.quit()
    sys.exit()

# Gestionar events
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
    return True

# Fer càlculs
def app_run(): 
    # para que de vueltas
    global girant, speed , voltes, angle
    max_voltes = random.randint(0,36) 
    if girant: # mientras gira se le suma velocidad y vueltas
        angle += speed
        if angle > 360:
            angle -= 360
            voltes += 1
        if voltes >= max_voltes: # si supera el max frena
            speed -= 1
        if speed <= 0:
            girant = False
            speed = 0


# investigar como hacer que detecte el num 
# angulo aprox quesito 9.7
# math.floor > redondea hacia abajo
# https://www.youtube.com/watch?v=WIIf3WaO5x4
# 

        
        


# Dibuixar

def app_draw():
    
    # Pintar el fons de blanc
    screen.fill(WHITE)

    # Dibuixar la graella
    utils.draw_grid(pygame, screen, 50)

    # Dibuixar les dades
    center = {"x": 300, "y": 250}
    
    for i,casella in enumerate(rule): 
        inici_angle = (360 / 37) * i + angle # donde empieza el angulo pa dibujar el quesito
        fi_angle = (360 / 37) * (i + 1) + angle #donde acaba.

        #PUNTS POLIGON(CIRCULO GRANDE)
        p0 = utils.point_on_circle(center,100,inici_angle)
        p1 = utils.point_on_circle(center,150,inici_angle)
        p2 = utils.point_on_circle(center,150,fi_angle)
        p3 = utils.point_on_circle(center,100,fi_angle)

        #PUNTS POLIGON PETIT(CIRCULO PEQUEÑOS)
        p0_petit = utils.point_on_circle(center,50,inici_angle)
        p1_petit = utils.point_on_circle(center,100,inici_angle)
        p2_petit = utils.point_on_circle(center,100,fi_angle)
        p3_petit = utils.point_on_circle(center,50,fi_angle)


        #COLORES RULETA
        if i == 0:  
            color = GREEN
        elif i % 2 == 1: 
            color = BLACK
        else:  
            color = RED       
        #DICCIONARIOS CON COORDENADAS
        points = [ #CIRCULO GRANDE
            (int(p0["x"]), int(p0["y"])),
            (int(p1["x"]), int(p1["y"])),
            (int(p2["x"]), int(p2["y"])),
            (int(p3["x"]), int(p3["y"]))
        ]

        points_petit = [ #CIRCULO PEQUEÑO
            (int(p0_petit["x"]), int(p0_petit["y"])),
            (int(p1_petit["x"]), int(p1_petit["y"])),
            (int(p2_petit["x"]), int(p2_petit["y"])),
            (int(p3_petit["x"]), int(p3_petit["y"]))
        ]

        coords = [ #FLECHITA
        ((290),(90)),
        ((310),(90)),
        ((300),(115))

    ]


        # Draw polygon between consecutive lines
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, color, points_petit)
        centre_quesito = utils.point_on_circle(center,140,(inici_angle + fi_angle) / 2)
        fontnum = pygame.font.SysFont("Arial", 15)
        if color == BLACK:
            color_num = WHITE
        else:
            color_num = BLACK   
            


        txt = fontnum.render(str(casella), True, color_num)


        pygame.draw.rect(screen, BLACK, (buttons[0]["x"], buttons[0]["y"], buttons[0]["width"], buttons[0]["height"]), 5) #boton(provisional)



        screen.blit(txt, (int(centre_quesito["x"] - txt.get_width() / 2), int(centre_quesito["y"] - txt.get_height() / 2))) #dibuja los numeros en cada questio(del medio de cada quesito)
        pygame.draw.circle(screen,WHITE,(300,250),100,5)
        pygame.draw.polygon(screen,(255,255,0),coords,3)
    pygame.draw.circle(screen,BLUE,(300,90),5,5)
        # Actualitzar el dibuix a la finestra
    pygame.display.update()


def girar_ruleta(): #PARA RESETEAR VALORES
    global girant,speed,voltes,angle 
    girant = True
    speed = 50
    voltes = 0
    angle = 0


if __name__ == "__main__":
    main()