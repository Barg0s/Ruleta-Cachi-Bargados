import pygame
import sys

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
    {"nom": "Bargos", "diners": 100, "fitxes": {"5": 5, "10": 1, "20": 0, "50": 0, "100": 2}, "aposta": [], "color": (50, 120, 200)},
    {"nom": "Cachi", "diners": 100, "fitxes": {"5": 0, "10": 5, "20": 1, "50": 2, "100": 0}, "aposta": [], "color": (200, 50, 50)},
    {"nom": "Albert", "diners": 100, "fitxes": {"5": 1, "10": 0, "20": 0, "50": 0, "100": 3}, "aposta": [], "color": (50, 200, 50)}
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

def create_betting_buttons():
    buttons = []
    y = button_start_y
    for row in betting_table:
        x = button_start_x
        for number in row:
            if number == 0:
                color = GREEN
            elif number in rojos:
                color = RED
            elif number in negros:
                color = BLACK
            button = {'number': number, 'x': x, 'y': y, 'height': button_height, 'width': button_width, 'color': color}
            buttons.append(button)
            x += button_width
        y += button_height
    return buttons

betting_buttons = create_betting_buttons()

def draw_betting_buttons():
    for button in betting_buttons:
        pygame.draw.rect(screen, button['color'], (button['x'], button['y'], button['width'], button['height']))
        pygame.draw.rect(screen, WHITE, (button['x'], button['y'], button['width'], button['height']), 1)
        font = pygame.font.SysFont("Arial", 15)
        label = font.render(str(button['number']), True, WHITE if button['color'] == BLACK else BLACK)
        screen.blit(label, (button['x'] + (button_width - label.get_width()) / 2, button['y'] + (button_height - label.get_height()) / 2))

def add_chips_for_current_player():
    global chips
    chips = []
    jugador = jugadors[turno_actual]
    x_base = 200
    y_base = 150
    radius = 20
    y_spacing = 30
    for valor, cantidad in jugador["fitxes"].items():
        y = y_base
        for _ in range(cantidad):
            chips.append({'value': int(valor), 'color': jugador["color"], 'x': x_base, 'y': y, 'radius': radius, 'owner': jugador["nom"]})
            y += y_spacing
        x_base += 70

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
                        num = button['number']
                        jugador = next(jugador for jugador in jugadors if jugador["nom"] == dragging_chip["owner"])
                        jugador["fitxes"][str(dragging_chip['value'])] -= 1
                        col = (button['x'] - carton_pos[0]) // carton_casilla_ancho
                        row = (button['y'] - carton_pos[1]) // carton_casilla_alto
                        x_pos = carton_pos[0] + col * carton_casilla_ancho + carton_casilla_ancho // 2
                        y_pos = carton_pos[1] + row * carton_casilla_alto + carton_casilla_alto // 2
                        dragging_chip['x'] = x_pos
                        dragging_chip['y'] = y_pos
                        apuestas.append({'jugador': dragging_chip['owner'], 'numero': num, 'value': dragging_chip['value'], 'color': dragging_chip['color']})
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

def draw_chips():
    for chip in chips:
        pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
        font = pygame.font.Font(None, 24)
        text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
        screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))

def draw_apuestas():
    for apuesta in apuestas:
        col = (apuesta['numero'] - 1) % 12
        row = (apuesta['numero'] - 1) // 12
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
        draw_betting_buttons()
        draw_apuestas()
        draw_chips()
        pygame.draw.rect(screen, BLUE, boton_rect)
        font = pygame.font.Font(None, 30)
        label = font.render('Cambiar Turno', True, WHITE)
        screen.blit(label, (boton_rect.x + (boton_rect.width - label.get_width()) / 2, boton_rect.y + (boton_rect.height - label.get_height()) / 2))
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
