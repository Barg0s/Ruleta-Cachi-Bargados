#!/usr/bin/env python3

import pygame
import sys
import utils
import random
import tauler as t
import jugadors as j
import fichas as f
import jugadors_dades as jd
import historial as h
import surface as s
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
circulo_ruleta = pygame.image.load("circuloruleta.png")
fondo = pygame.image.load("casinofondo.png")
buen_fondo = pygame.transform.scale(fondo,(860,680))
pygame.init()
clock = pygame.time.Clock()
historial_ganador = []
historial_complet = []
chips = []
apuestas = []
rule = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
angulo_actual = 265
girando = False
angulo_velocidad = 0
seleccionado = None
idx = 0
mostrar_surface = False
apostar = False
# Definir la finestra
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Ruleta')
mouse = {'x': -1, 'y': -1,'pressed': False}
font = pygame.font.SysFont("Arial",22)
carton_pos = (100, 450)
carton_casilla_ancho = 50
carton_casilla_alto = 50
carton_filas = 3
carton_columnas = 12
valors_fitxes = ([5,10,20,50,100])
dragging_chip = None
offset_x, offset_y = 0, 0
close_button_rect = {
        "x": 860 - 60,
        "y": 10,
        "width": 50,
        "height": 25,
    }
# Definir botones
buttons = [
    {'name': 'Girar', 'x': 500, 'y': 400, 'width': 100, 'height': 50, 'pressed': False},
    {'name': 'Apostar', 'x': 650, 'y': 400, 'width': 100, 'height': 50, 'pressed': False},
    {'name': 'Log', 'x': 650, 'y': 250, 'width': 100, 'height': 50, 'pressed': False}
]
girando = False

def afegir_fitxes():
    """Añade las fichas del jugador actual."""
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



def dibuixar_fitxes():
    """Dibuja las fichas activas y permite arrastrarlas."""
    for chip in chips:

        pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
        pygame.draw.circle(screen, BLACK, (chip['x'], chip['y']), chip['radius'],1)
        pygame.draw.circle(screen, WHITE, (chip['x'], chip['y']), chip['radius'] - 5)
        font = pygame.font.Font(None, 24)
        text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
        screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))

def dibuixar_apostes():
    for apuesta in apuestas:
        if apuesta.get('posicion') >= 0:  # Para las casillas normales
            col = apuesta['posicion'] % carton_columnas
            row = apuesta['posicion'] // carton_columnas
            x = carton_pos[0] + col * carton_casilla_ancho + carton_casilla_ancho // 2
            y = carton_pos[1] + row * carton_casilla_alto + carton_casilla_alto // 2
        else:  # Para las casillas especiales
            button = next(b for b in t.custom_buttons if b['label'] == apuesta['label'])
            x = button['x'] + button['width'] // 2
            y = button['y'] + button['height'] // 2
        pygame.draw.circle(screen, apuesta['color'], (x, y), 20)
        pygame.draw.circle(screen, BLACK, (x, y), 20,1)
        pygame.draw.circle(screen, WHITE, (x, y), 15)
        font = pygame.font.Font(None, 24)
        text = font.render(str(apuesta['value']), True, BLACK if apuesta['color'] != BLACK else WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


# Bucle de la aplicación
def main():
    is_looping = True
    afegir_fitxes() 
    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60)  # Limitar a 60 FPS

    # Fuera del bucle, cerrar la aplicación
    pygame.quit()
    sys.exit()

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
            h.gestionar_nums(historial_ganador,seleccionado)
            print(apuestas)
            h.guardar_torn(historial_complet,f"Ha sortit el numero: {seleccionado}")
            print(f"Seleccionado: {seleccionado}")
            print("AAAAAAAAAAAAAAAAA")
            print(apuestas)
            print(f.obtener_valores_apuestas(seleccionado,apuestas,j.banca))
            f.comprobar_aposta(seleccionado,apuestas,historial_complet)

            apuestas.clear()
            for jugador in j.jugadors:
                jugador["tipus"] = ""

# Gestionar eventos
dragging_chip = None  # Ficha actualmente siendo arrastrada
offset_x, offset_y = 0, 0  # Desplazamiento del ratón

    




def app_events():
    global mouse, angulo_actual, girando, angulo_velocidad, seleccionado, apostar, idx, dragging_chip, offset_x, offset_y,mostrar_surface
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEMOTION:
            mouse['x'], mouse['y'] = event.pos
            # Si se está arrastrando una ficha, actualizar su posición
            if dragging_chip:
                dragging_chip['x'] = mouse['x'] - offset_x
                dragging_chip['y'] = mouse['y'] - offset_y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hace clic en alguna ficha
            for chip in chips:
                if (mouse['x'] - chip['x'])**2 + (mouse['y'] - chip['y'])**2 <= chip['radius']**2:  # Si el clic está dentro de la ficha
                    dragging_chip = chip  # Empezar a arrastrar esta ficha
                    offset_x = mouse['x'] - chip['x']
                    offset_y = mouse['y'] - chip['y']
                    break
            # Si no se está arrastrando ninguna ficha, verifica si se hace clic en los botones

            if not dragging_chip:
                for button in buttons:
                    afegir_fitxes() 
                    if utils.is_point_in_rect(mouse, button) and not girando and button['name'] == "Girar":
                        girando = True
                        angulo_velocidad = random.randint(5, 37)  # Velocidad random
                        print("¡Girando!")
                    elif utils.is_point_in_rect(mouse, button) and not girando and button['name'] == "Log":
                        mostrar_surface = True
                    elif utils.is_point_in_rect(mouse, button) and not girando and button['name'] == "Apostar":
                        apostar = True
                        print("Apuesta hecha!")
                        idx = jd.gestio_turns(screen, font, j.jugadors, idx, apostar)
                         # Añadir fichas para el siguiente jugador
                        apostar = False
                        f.distribuir_fitxes(j.jugadors,valors_fitxes)
                        afegir_fitxes()


        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_chip:
                # Verificar casillas normales
                for button in t.betting_buttons:
                    if utils.is_point_in_rect({'x': dragging_chip['x'], 'y': dragging_chip['y']}, button):
                        col = (button['x'] - carton_pos[0]) // carton_casilla_ancho
                        row = (button['y'] - carton_pos[1]) // carton_casilla_alto
                        pos = row * carton_columnas + col
                        jugador_actual = None
                        for jugador in j.jugadors:
                            if jugador["nom"] == dragging_chip["owner"]:
                                jugador_actual = jugador
                                break                        
                        jugador_actual["fitxes"][str(dragging_chip['value'])] -= 1
                        x_pos = carton_pos[0] + col * carton_casilla_ancho + carton_casilla_ancho // 2
                        y_pos = carton_pos[1] + row * carton_casilla_alto + carton_casilla_alto // 2
                        dragging_chip['x'] = x_pos
                        dragging_chip['y'] = y_pos
                        apuestas.append({'jugador': dragging_chip['owner'], 'posicion': pos, 'value': dragging_chip['value'], 'color': dragging_chip['color']})

                        numero = t.betting_table[row][col]
                        h.guardar_torn(historial_complet,f"Aposta feta al {numero} amb {dragging_chip['value']} per {dragging_chip['owner']}")
                        print(f"Ficha colocada por {dragging_chip['owner']} en el número {numero}")
                        j.jugadors[idx]["diners"] -= dragging_chip['value']
                        j.jugadors[idx]["aposta"].append(numero)
                        j.jugadors[idx]["tipus"] = "Individual"
                        print(j.jugadors[idx]["aposta"])
                        chips.remove(dragging_chip)
                        break
                else:
                    # Verificar casillas especiales
                    for button in t.custom_buttons:
                        if utils.is_point_in_rect({'x': dragging_chip['x'], 'y': dragging_chip['y']}, button):
                            print(f"Ficha colocada en {button['label']} por {dragging_chip['owner']}")
                            jugador_actual = None
                            for jugador in j.jugadors:
                                if jugador["nom"] == dragging_chip["owner"]:
                                    jugador_actual = jugador
                                    break  
                            jugador_actual["fitxes"][str(dragging_chip['value'])] -= 1
                            dragging_chip['x'] = button['x'] + button['width'] // 2
                            dragging_chip['y'] = button['y'] + button['height'] // 2
                            apuestas.append({'jugador': dragging_chip['owner'], 'posicion': -1, 'value': dragging_chip['value'], 'color': dragging_chip['color'], 'label': button['label']})
                            h.guardar_torn(historial_complet,f"Aposta feta a {button['label']} amb {dragging_chip['value']} per {dragging_chip['owner']}")
                            j.jugadors[idx]["diners"] -= dragging_chip['value']
                            j.jugadors[idx]["tipus"] = button['label']
                            f.gestionar_especials(idx,button['label'])
                            chips.remove(dragging_chip)
                            break
                    else:
                        if dragging_chip['value'] == 5:
                            dragging_chip['x'], dragging_chip['y'] = 800, 400
                        elif dragging_chip['value'] == 10:
                            dragging_chip['x'], dragging_chip['y'] = 800, 460
                        elif dragging_chip['value'] == 20:
                            dragging_chip['x'], dragging_chip['y'] = 800, 520
                        elif dragging_chip['value'] == 50:
                            dragging_chip['x'], dragging_chip['y'] = 800, 580
                        else:
                            dragging_chip['x'], dragging_chip['y'] = 800, 640

                dragging_chip = None
        elif event.type == pygame.MOUSEMOTION and dragging_chip:
            mouse_pos = pygame.mouse.get_pos()
            dragging_chip['x'] = mouse_pos[0] - offset_x
            dragging_chip['y'] = mouse_pos[1] - offset_y
    girar_ruleta()

    return True
def app_run(): 
    pass  


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

def app_draw():
    global mostrar_surface
    # Pintar el fondo de blanco
    screen.fill(WHITE)
    screen.blit(buen_fondo, (0, 0))  # Fondo de casino
    jd.dibuixar_banca(screen,font,j.banca)
    t.draw_custom_buttons(screen)  # Dibujar botones personalizados
    t.draw_betting_buttons(screen)  # Dibujar botones de apuestas
    jd.gestio_turns(screen, font, j.jugadors, idx, apostar)  # Mostrar turno del jugador
    pygame.draw.circle(screen, CENICA, (300, 250), 100)  # Dibujar el círculo de la ruleta
    utils.draw_grid(pygame, screen, 50)

    screen.blit(circulo_ruleta, (230, 180))  # Dibujar la imagen de la ruleta
    pygame.draw.circle(screen, GOLD, (300, 250), 100, 5)  # Círculos de bordes dorados
    pygame.draw.circle(screen, GOLD, (300, 250), 70, 5)
    pygame.draw.circle(screen, GOLD, (300, 250), 154, 5)  # Más bordes

    dibujar_ruleta()  # Dibujar las casillas de la ruleta

    for button in buttons:
        # Dibujar botones de la interfaz
        text_girar = font.render(buttons[0]["name"], True, WHITE)
        text_apostar = font.render(buttons[1]["name"], True, WHITE)
        text_log = font.render(buttons[2]["name"], True, WHITE)
        pygame.draw.rect(screen, MARRON, (button["x"], button["y"], button["width"], button["height"]))  # Botón
        pygame.draw.rect(screen, BLACK, (button["x"], button["y"], button["width"], button["height"]), 5)  # Borde del botón
        screen.blit(text_girar, (525, 415))
        screen.blit(text_apostar, (665, 415))
        screen.blit(text_log, (680, 265))

    h.mostrar_guanyadors(screen, seleccionado, historial_ganador)  # Mostrar historial de ganadores

    # Dibujar fichas y apuestas
    dibuixar_fitxes()
    dibuixar_apostes()
    f.contar_fitxes(screen,idx)
    if mostrar_surface:
        mostrar_surface = s.events_surface(mouse, close_button_rect, mostrar_surface)

        # Dibujar todo en la pantalla
        s.draw_surface()
        s.draw_scroll_slider()
        s.dibuixar_historial(historial_complet)
        s.draw_close_button(close_button_rect)

        # Actualizar la posición del scroll
        s.update_scroll_position(mouse)
        print(mostrar_surface)
        pygame.display.update()  # Actualizar la pantalla
    pygame.display.update()  # Actualizar la pantalla




if __name__ == "__main__":
    main()