#!/usr/bin/env python3

import pygame
import sys
import utils
import random
import tauler as t
import jugadors as j
import jugadors_dades as jd
import fichas as f
# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (255, 0, 0)  
GREEN = (0, 255, 0)
MARRON = (151, 91, 57)
GOLD = (255,215,0)
CENICA = (138,149,151)
VERDE = (0, 100, 0)
dragging_chip = None
offset_x, offset_y = 0, 0

circulo_ruleta = pygame.image.load("circuloruleta.png")
fondo = pygame.image.load("casinofondo.png")
buen_fondo = pygame.transform.scale(fondo,(860,680))
pygame.init()
clock = pygame.time.Clock()
historial_ganador = []
rule = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
angulo_actual = 265
girando = False
angulo_velocidad = 0
seleccionado = None
idx = 0
apostar = False
# Definir la finestra
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Ruleta')
mouse = {'x': -1, 'y': -1}
font = pygame.font.SysFont("Arial",22)

# Definir botones
buttons = [
    {'name': 'Girar', 'x': 500, 'y': 400, 'width': 100, 'height': 50, 'pressed': False},
    {'name': 'Apostar', 'x': 650, 'y': 400, 'width': 100, 'height': 50, 'pressed': False}
]

# Bucle de la aplicación
def main():
    is_looping = True

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()
        draw_apuestas()
        clock.tick(60)  # Limitar a 60 FPS

    # Fuera del bucle, cerrar la aplicación
    pygame.quit()
    sys.exit()
chips = []
apuestas = []
carton_columnas = 50
carton_casilla_ancho = 50

carton_casilla_alto = 50
def add_chips_for_current_player(idx):
    global chips
    chips = []
    jugador = j.jugadors[idx]
    x_base = 800
    y_base = 400
    radius = 20
    y_spacing = 5
    for valor, cantidad in jugador["fitxes"].items():
        y = y_base
        for _ in range(cantidad):
            chips.append({'value': int(valor), 'color': jugador["color"], 'x': x_base, 'y': y, 'radius': radius, 'owner': jugador["nom"]})
            y += y_spacing
        y_base += 60
def draw_apuestas():
    for apuesta in apuestas:
        col = apuesta['posicion'] % carton_columnas
        row = apuesta['posicion'] // carton_columnas
        x = 100 + col * carton_casilla_ancho + carton_casilla_ancho // 2
        y = 450 + row * carton_casilla_alto + carton_casilla_alto // 2
        pygame.draw.circle(screen, apuesta['color'], (x, y), 20)
        font = pygame.font.Font(None, 24)
        text = font.render(str(apuesta['value']), True, BLACK if apuesta['color'] != BLACK else WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

def draw_apuestas():
    for apuesta in apuestas:
        col = apuesta['posicion'] % carton_columnas
        row = apuesta['posicion'] // carton_columnas
        x = 100 + col * carton_casilla_ancho + carton_casilla_ancho // 2
        y = 450 + row * carton_casilla_alto + carton_casilla_alto // 2
        pygame.draw.circle(screen, apuesta['color'], (x, y), 20)
        font = pygame.font.Font(None, 24)
        text = font.render(str(apuesta['value']), True, BLACK if apuesta['color'] != BLACK else WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

def draw_chips():
    # Dibujar todas las fichas
    for chip in chips:
        # Verificar si la ficha está encima de algún botón especial
        for button in t.custom_buttons:
            button_rect = pygame.Rect(button['x'], button['y'], button['width'], button['height'])
            if button_rect.collidepoint(chip['x'], chip['y']):
                # Si la ficha está sobre un botón especial, dibujarla encima del botón
                pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
                font = pygame.font.Font(None, 24)
                text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
                screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))
                break
        else:
            # Si la ficha no está sobre un botón especial, dibujarla normalmente
            pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
            font = pygame.font.Font(None, 24)
            text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
            screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))


def girar_ruleta():
    global angulo_actual, angulo_velocidad, girando, seleccionado
    if girando:
        # Actualizar el ángulo actual
        angulo_actual += angulo_velocidad
        angulo_actual %= 360  # pa que el angulo no se pase de 360.
        angulo_velocidad *= 0.98  # bajar la velocidad suave

        if angulo_velocidad < 0.5:
            girando = False
            angulo_velocidad = 0

            # El numero ganador
            flecha_angulo = (270 - angulo_actual) % 360 # averiguar donde esta la flecha
            segmento = int(flecha_angulo // (360 / len(rule))) #saber donde cayó la flecha( el // es para que divida a la baja)
            seleccionado = rule[segmento] #usa el segmento como index de la lista rule y pilla esa pos
            gestionar_nums(seleccionado)
            print(f"Seleccionado: {seleccionado}")



def app_events():
    global mouse, angulo_actual, girando, angulo_velocidad, seleccionado, apostar, idx
    global turno_actual, dragging_chip, offset_x, offset_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            mouse['x'], mouse['y'] = event.pos
            if dragging_chip:
                # Actualiza la posición de la ficha mientras se arrastra
                dragging_chip['x'] = mouse['x'] - offset_x
                dragging_chip['y'] = mouse['y'] - offset_y

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Evento de clic en los botones de la interfaz
            for button in buttons:
                if utils.is_point_in_rect(mouse, button) and not girando and button['name'] == "Girar":
                    girando = True
                    angulo_velocidad = random.randint(5, 37)  # Velocidad random
                    print("¡Girando!")
                elif utils.is_point_in_rect(mouse, button) and not girando and button['name'] == "Apostar":
                    apostar = True
                    print("Apuesta hecha!")
                    idx = jd.gestio_turns(screen, font, j.jugadors, idx, apostar)  # Cambio de jugador
                    apostar = False  

            for button in t.betting_buttons:
                if utils.is_point_in_rect(mouse, button):
                    print(f"button {button['number']}!")

            for button_apostar in t.custom_buttons:
                if utils.is_point_in_rect(mouse, button_apostar):
                    print(f"Custom Button {button_apostar.get('label', 'RED/BLACK')} clicked!")  # Handle custom button click

            # Verificar si una ficha está siendo arrastrada
            for chip in chips:
                if utils.is_point_in_circle({'x': mouse_pos[0], 'y': mouse_pos[1]}, {'x': chip['x'], 'y': chip['y']}, chip['radius']):
                    dragging_chip = chip
                    offset_x = mouse_pos[0] - chip['x']
                    offset_y = mouse_pos[1] - chip['y']
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_chip:
                # Verificar si la ficha fue colocada en una casilla de apuestas normal
                for button in t.betting_buttons:
                    if utils.is_point_in_rect({'x': dragging_chip['x'], 'y': dragging_chip['y']}, button):
                        col = (button['x'] - 100) // carton_casilla_ancho
                        row = (button['y'] - 450) // carton_casilla_alto
                        pos = row * carton_columnas + col
                        jugador = next(jugador for jugador in j.jugadors if jugador["nom"] == dragging_chip["owner"])
                        jugador["fitxes"][str(dragging_chip['value'])] -= 1
                        x_pos = 100  + col * carton_casilla_ancho + carton_casilla_ancho // 2
                        y_pos = 450 + row * carton_casilla_alto + carton_casilla_alto // 2
                        dragging_chip['x'] = x_pos
                        dragging_chip['y'] = y_pos
                        apuestas.append({'jugador': dragging_chip['owner'], 'posicion': pos, 'value': dragging_chip['value'], 'color': dragging_chip['color']})

                        # Obtener el número de la betting_table
                        numero = t.betting_table[row][col]

                        # Imprimir la información
                        print(f"Ficha colocada por {dragging_chip['owner']} en el número {numero}")

                        chips.remove(dragging_chip)
                        break
                else:
                    # Si la ficha no fue colocada en una casilla normal, verificar casillas especiales
                    for button in t.custom_buttons:
                        if utils.is_point_in_rect({'x': dragging_chip['x'], 'y': dragging_chip['y']}, button):
                            # Casilla especial, procesar según el tipo de casilla
                            if button['label'] == '0':
                                print(f"Ficha colocada en el 0 por {dragging_chip['owner']}")
                            elif button['label'] == 'PAR':
                                print(f"Ficha colocada en PAR por {dragging_chip['owner']}")
                            elif button['label'] == 'RED':
                                print(f"Ficha colocada en RED por {dragging_chip['owner']}")
                            elif button['label'] == 'BLACK':
                                print(f"Ficha colocada en BLACK por {dragging_chip['owner']}")
                            elif button['label'] == 'IMP':
                                print(f"Ficha colocada en IMP por {dragging_chip['owner']}")
                            elif button['label'] == '2 to 1':  # Si es una casilla '2 to 1'
                                print(f"Ficha colocada en 2 to 1 por {dragging_chip['owner']}")
                            
                            # Coloca la ficha en el centro del botón especial
                            dragging_chip['x'] = button['x'] + button['width'] // 2
                            dragging_chip['y'] = button['y'] + button['height'] // 2

                            # Quitar la ficha de la lista de fichas y agregar la apuesta
                            chips.remove(dragging_chip)
                            break
                    else:
                        # Si no se ha soltado en ninguna casilla especial ni de apuestas
                        dragging_chip['x'] = 200
                        dragging_chip['y'] = 150

                dragging_chip = None
        
        # Llamar a la función que controla el giro de la ruleta
        girar_ruleta()

    return True



def app_run(): 
    pass  

def gestionar_nums(num):
    historial_ganador.append(num)
    if len(historial_ganador) > 10:
        historial_ganador.pop(0)
def dibujar_ruleta():
    center = {"x": 300, "y": 250}

    for i, casella in enumerate(rule):
        inici_angle = (360 / 37) * i  # Ángulo inicial para dibujar cada casilla
        fi_angle = (360 / 37) * (i + 1)  # Ángulo final

        # PUNTOS DEL POLÍGONO (CÍRCULO GRANDE)
        p0 = utils.point_on_circle(center, 100, inici_angle + angulo_actual)
        p1 = utils.point_on_circle(center, 150, inici_angle + angulo_actual)
        p2 = utils.point_on_circle(center, 150, fi_angle + angulo_actual)
        p3 = utils.point_on_circle(center, 100, fi_angle + angulo_actual)

        # COLORES DE LA RULETA
        if i == 0:  
            color = GREEN
        elif i % 2 == 1: 
            color = RED
        else:  
            color = BLACK       

        # DICCIONARIOS CON COORDENADAS
        points = [  # CÍRCULO GRANDE
            (int(p0["x"]), int(p0["y"])),
            (int(p1["x"]), int(p1["y"])),
            (int(p2["x"]), int(p2["y"])),
            (int(p3["x"]), int(p3["y"]))
        ]

        # DIBUJAR FLECHA
        coords_flecha = [
            (300 - 10, 80),
            (300 + 10, 80),
            (300, 105)
        ]
        pygame.draw.polygon(screen, BLUE, coords_flecha)
        pygame.draw.polygon(screen, BLACK, coords_flecha, 2)

        # Dibujar los polígonos
        pygame.draw.polygon(screen, color, points)

        # Dibujar el número en el centro de cada casilla
        centre_quesito = utils.point_on_circle(center, 140, (inici_angle + fi_angle) / 2 + angulo_actual)
        fontnum = pygame.font.SysFont("Arial", 15)
        if color == BLACK:
            color_num = WHITE
        else:
            color_num = BLACK   

        txt = fontnum.render(str(casella), True, color_num)
        screen.blit(txt, (int(centre_quesito["x"] - txt.get_width() / 2), int(centre_quesito["y"] - txt.get_height() / 2)))  # Dibujar el número en cada casilla

# Función para dibujar el historial de los ganadores
# Dibujar

def app_draw():
    # Pintar el fondo de blanco

    screen.fill(WHITE)
    # Dibujar la cuadrícula
    
    screen.blit(buen_fondo,(0,0))
    utils.draw_grid(pygame, screen, 50)

    t.draw_custom_buttons(screen)
    t.draw_betting_buttons(screen)
    jd.gestio_turns(screen,font,j.jugadors,idx,apostar)
    pygame.draw.circle(screen,CENICA,(300,250),100)   

    screen.blit(circulo_ruleta, (230, 180))

    pygame.draw.circle(screen,GOLD,(300,250),100,5)    
    pygame.draw.circle(screen,GOLD,(300,250),70,5)
    pygame.draw.circle(screen,GOLD,(300,250),154,5)   

   
    dibujar_ruleta()

    for button in buttons:
        text_girar = font.render(buttons[0]["name"],True, WHITE)
        text_apostar = font.render(buttons[1]["name"],True, WHITE)
        pygame.draw.rect(screen, MARRON, (button["x"], button["y"], button["width"], button["height"])) #boton(provisional)
        pygame.draw.rect(screen, BLACK, (button["x"], button["y"], button["width"], button["height"]), 5) #boton(provisional)    screen.blit(text_girar,(525, 415))
        screen.blit(text_girar,(525, 415))
        screen.blit(text_apostar,(665, 415))

    mostrar_guanyadors()
    add_chips_for_current_player(idx)
    draw_chips()
    pygame.display.update()


def mostrar_guanyadors():
    # Actualizar la pantalla
    if seleccionado is not None:
        x = 430
        for num in historial_ganador: 
            texto_seleccion = font.render(f"{num},", True, BLACK)
            screen.blit(texto_seleccion, (x - texto_seleccion.get_width() // 2, 100))
            x += 35

if __name__ == "__main__":
    main()
