import pygame
import sys
import tauler as t
import utils
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (50, 120, 200)
GREEN = (0, 255, 0)
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Roulette Game')

chips = []
apuestas = []
mouse = {'x': -1, 'y': -1}

button_start_x = 100
button_start_y = 450
button_width = 50
button_height = 50

betting_table = [
    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
    [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
]

rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

jugadors = [
    {"nom": "Bargos", "diners": 100, "fitxes": {"5": 5, "10": 1, "20": 0, "50": 0, "100": 2}, "aposta": [], "color": (255,128,0) },
    {"nom": "Cachi", "diners": 100, "fitxes": {"5": 0, "10": 5, "20": 1, "50": 2, "100": 0}, "aposta": [], "color": (204,169,221)},
    {"nom": "Albert", "diners": 100, "fitxes": {"5": 1, "10": 0, "20": 0, "50": 0, "100": 3}, "aposta": [], "color": (50, 120,200)}
]
turno_actual = 0
boton_rect = pygame.Rect(700, 20, 140, 40)

dragging_chip = None
offset_x, offset_y = 0, 0

carton_pos = (100, 450)
carton_casilla_ancho = 50
carton_casilla_alto = 50
carton_filas = 3
carton_columnas = 12



def add_chips_for_current_player():
    global chips
    chips = []
    jugador = jugadors[turno_actual]
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
def app_events():
    global turno_actual, dragging_chip, offset_x, offset_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if boton_rect.collidepoint(mouse_pos):
                turno_actual = (turno_actual + 1) % len(jugadors)
                add_chips_for_current_player()
            
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

                        # Obtener el número de la betting_table
                        numero = betting_table[row][col]

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
        
        elif event.type == pygame.MOUSEMOTION and dragging_chip:
            mouse_pos = pygame.mouse.get_pos()
            dragging_chip['x'] = mouse_pos[0] - offset_x
            dragging_chip['y'] = mouse_pos[1] - offset_y


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


def draw_apuestas():
    for apuesta in apuestas:
        col = apuesta['posicion'] % carton_columnas
        row = apuesta['posicion'] // carton_columnas
        x = carton_pos[0] + col * carton_casilla_ancho + carton_casilla_ancho // 2
        y = carton_pos[1] + row * carton_casilla_alto + carton_casilla_alto // 2
        pygame.draw.circle(screen, apuesta['color'], (x, y), 20)
        font = pygame.font.Font(None, 24)
        text = font.render(str(apuesta['value']), True, BLACK if apuesta['color'] != BLACK else WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

def main():
    global screen, turno_actual
    add_chips_for_current_player()
    while True:
        screen.fill(DARK_GRAY)
        app_events()
        t.draw_custom_buttons(screen)  # Dibuja primero los botones especiales

        t.draw_betting_buttons(screen)
        draw_apuestas()
        draw_chips()  # Dibuja las fichas después de los botones
        pygame.draw.rect(screen, BLUE, boton_rect)
        font = pygame.font.Font(None, 24)
        text = font.render(f"Jugador: {jugadors[turno_actual]['nom']}", True, WHITE)
        screen.blit(text, (20, 20))
        pygame.draw.rect(screen, BLUE, boton_rect)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
