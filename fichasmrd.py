# fichas.py
import pygame
import sys
from tauler import create_betting_buttons, draw_betting_buttons, draw_custom_buttons
BLACK = (0,0,0)
WHITE = 255,255,255
carton_pos = (100, 450)
carton_casilla_ancho = 50
carton_casilla_alto = 50
carton_filas = 3
carton_columnas = 12
def add_chips_for_current_player(jugadors, turno_actual):
    chips = []
    jugador = jugadors[turno_actual]
    x_base = 200
    y_base = 150
    radius = 20
    y_spacing = 5
    for valor, cantidad in jugador["fitxes"].items():
        y = y_base
        for _ in range(cantidad):
            chips.append({'value': int(valor), 'color': jugador["color"], 'x': x_base, 'y': y, 'radius': radius, 'owner': jugador["nom"]})
            y += y_spacing
        y_base += 60
    return chips
boton_rect = pygame.Rect(700, 20, 140, 40)

def draw_chips(screen, chips):
    for chip in chips:
        pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
        font = pygame.font.Font(None, 24)
        text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
        screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))

def app_events(screen, chips, betting_buttons, custom_buttons, jugadors, turno_actual, dragging_chip, offset_x, offset_y, apuestas):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if boton_rect.collidepoint(mouse_pos):
                turno_actual = (turno_actual + 1) % len(jugadors)
                chips = add_chips_for_current_player(jugadors, turno_actual)
            for chip in chips:
                dx = mouse_pos[0] - chip['x']
                dy = mouse_pos[1] - chip['y']
                if (dx ** 2 + dy ** 2) <= chip['radius'] ** 2:
                    dragging_chip = chip
                    offset_x = dx
                    offset_y = dy
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_chip:
                for button in betting_buttons:
                    button_rect = pygame.Rect(button['x'], button['y'], button['width'], button['height'])
                    if button_rect.collidepoint(dragging_chip['x'], dragging_chip['y']):
                        col = (button['x'] - carton_pos[0]) // carton_casilla_ancho
                        row = (button['y'] - carton_pos[1]) // carton_casilla_alto
                        pos = row * carton_columnas + col
                        jugador = next(jugador for jugador in jugadors if jugador["nom"] == dragging_chip["owner"])
                        jugador["fitxes"][str(dragging_chip['value'])] -= 1
                        x_pos = carton_pos[0] + col * carton_casilla_ancho + carton_casilla_ancho // 2
                        y_pos = carton_pos[1] + row * carton_casilla_alto + carton_casilla_alto // 2
                        dragging_chip['x'] = x_pos
                        dragging_chip['y'] = y_pos
                        apuestas.append({'jugador': dragging_chip['owner'], 'posicion': pos, 'value': dragging_chip['value'], 'color': dragging_chip['color']})

                        chips.remove(dragging_chip)
                        break
                else:
                    for button in custom_buttons:
                        button_rect = pygame.Rect(button['x'], button['y'], button['width'], button['height'])
                        if button_rect.collidepoint(dragging_chip['x'], dragging_chip['y']):
                            dragging_chip['x'] = button['x'] + button['width'] // 2
                            dragging_chip['y'] = button['y'] + button['height'] // 2
                            chips.remove(dragging_chip)
                            break
                    else:
                        dragging_chip['x'] = 200
                        dragging_chip['y'] = 150
                dragging_chip = None
        elif event.type == pygame.MOUSEMOTION and dragging_chip:
            mouse_pos = pygame.mouse.get_pos()
            dragging_chip['x'] = mouse_pos[0] - offset_x
            dragging_chip['y'] = mouse_pos[1] - offset_y

