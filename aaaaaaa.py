import pygame
import sys

# Inicialización de Pygame y configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
pygame.init()
clock = pygame.time.Clock()

# Configuración de la ventana y parámetros
screen = pygame.display.set_mode((860, 680))
pygame.display.set_caption('Roulette Game')
orden_tablero = [32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

chips = []  # Lista para todas las fichas activas en el tablero
apuestas = []  # Lista de apuestas realizadas
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

# Datos de los jugadores
jugadors = [
    {
        "nom": "Bargos",
        "diners": 100,
        "fitxes": {"5": 5, "10": 1, "20": 0, "50": 0, "100": 2},
        "aposta": [],
        "color": (50, 120, 200)  # Azul
    },
    {
        "nom": "Cachi",
        "diners": 100,
        "fitxes": {"5": 0, "10": 5, "20": 1, "50": 2, "100": 0},
        "aposta": [],
        "color": (200, 50, 50)  # Rojo
    },
    {
        "nom": "Albert",
        "diners": 100,
        "fitxes": {"5": 1, "10": 0, "20": 0, "50": 0, "100": 3},
        "aposta": [],
        "color": (50, 200, 50)  # Verde
    }
]

# Control de turnos
turno_actual = 0  # Índice del jugador que tiene el turno

# Botón para cambiar de turno
boton_rect = pygame.Rect(700, 20, 140, 40)

# Variables de control para arrastrar fichas
dragging_chip = None  # Indica qué ficha se está arrastrando
offset_x, offset_y = 0, 0  # Compensación entre el clic y el centro de la ficha

# Definir cartón de apuestas
carton_pos = (50, 500)  # Posición del cartón
carton_casilla_ancho = 60  # Ancho de cada casilla
carton_casilla_alto = 60  # Alto de cada casilla
carton_filas = 3
carton_columnas = 12

definir_carton = pygame.Rect(carton_pos[0], carton_pos[1], 
                              carton_columnas * carton_casilla_ancho, 
                              carton_filas * carton_casilla_alto)

# Función para agregar fichas activas del jugador actual
def add_chips_for_current_player():
    global chips
    chips = []  # Reiniciar las fichas para mostrar solo las del jugador actual
    jugador = jugadors[turno_actual]
    x_base = 200  # Posición inicial en el eje X
    y_base = 150  # Posición inicial en el eje Y
    radius = 20  # Radio de la ficha
    y_spacing = 30  # Espaciado vertical para apilar

    for valor, cantidad in jugador["fitxes"].items():
        y = y_base
        for _ in range(cantidad):
            chips.append({
                'value': int(valor),
                'color': jugador["color"],
                'x': x_base,
                'y': y,
                'radius': radius,
                'owner': jugador["nom"]
            })
            y += y_spacing  # Apilar las fichas del mismo valor
        x_base += 70  # Separar columnas de valores diferentes

# Eventos del programa principal
def app_events():
    global turno_actual, dragging_chip, offset_x, offset_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Verificar si se hace clic en el botón de cambio de turno
            if boton_rect.collidepoint(mouse_pos):
                turno_actual = (turno_actual + 1) % len(jugadors)
                add_chips_for_current_player()  # Actualizar fichas para el jugador actual

            # Verificar si se hace clic en alguna ficha para arrastrarla
            for chip in chips:
                dx = mouse_pos[0] - chip['x']
                dy = mouse_pos[1] - chip['y']
                if (dx ** 2 + dy ** 2) <= chip['radius'] ** 2:  # Dentro del círculo
                    dragging_chip = chip
                    offset_x = dx
                    offset_y = dy
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_chip:
                # Verificar si la ficha se coloca en una casilla válida del cartón
                col = (dragging_chip['x'] - definir_carton.x) // carton_casilla_ancho
                fil = (dragging_chip['y'] - definir_carton.y) // carton_casilla_alto

                # Comprobar si está dentro de los límites del cartón
                if 0 <= col < carton_columnas and 0 <= fil < carton_filas:
                    num = orden_tablero[fil * carton_columnas + col]  # Número de la casilla

                    # Comprobar si el número es válido (1-36)
                    if 1 <= num <= 36:
                        # Restar la ficha del jugador
                        jugador = next(jugador for jugador in jugadors if jugador["nom"] == dragging_chip["owner"])
                        jugador["fitxes"][str(dragging_chip['value'])] -= 1
                        
                        # Añadir la apuesta
                        apuestas.append({
                            'jugador': dragging_chip['owner'],
                            'numero': num,
                            'value': dragging_chip['value'],
                            'color': dragging_chip['color']
                        })
                        chips.remove(dragging_chip)  # Eliminar la ficha del tablero
                        print(f"Ficha de {dragging_chip['owner']} colocada en el número {num}")
                    else:
                        # Si la ficha no está en una casilla válida, vuelve a su posición inicial
                        dragging_chip['x'] = 200
                        dragging_chip['y'] = 150

                dragging_chip = None  # Finalizar el arrastre de ficha

        elif event.type == pygame.MOUSEMOTION and dragging_chip:
            # Actualiza la posición de la ficha mientras se arrastra
            mouse_pos = pygame.mouse.get_pos()
            dragging_chip['x'] = mouse_pos[0] - offset_x
            dragging_chip['y'] = mouse_pos[1] - offset_y
# Dibuja las fichas en la pantalla
def draw_chips():
    for chip in chips:
        pygame.draw.circle(screen, chip['color'], (chip['x'], chip['y']), chip['radius'])
        font = pygame.font.Font(None, 24)
        text = font.render(str(chip['value']), True, BLACK if chip['color'] != BLACK else WHITE)
        screen.blit(text, (chip['x'] - text.get_width() // 2, chip['y'] - text.get_height() // 2))

# Dibujar las apuestas realizadas
def draw_apuestas():
    for apuesta in apuestas:
        num = apuesta['numero']
        # Obtener la posición en el tablero de acuerdo con el orden de la casilla
        index = orden_tablero.index(num)
        col = index % 12  # Columna según el número de casilla
        row = index // 12  # Fila según el número de casilla
        x = carton_pos[0] + col * carton_casilla_ancho + carton_casilla_ancho // 2
        y = carton_pos[1] + row * carton_casilla_alto + carton_casilla_alto // 2
        pygame.draw.circle(screen, apuesta['color'], (x, y), 20)
        font = pygame.font.Font(None, 24)
        text = font.render(str(apuesta['value']), True, BLACK if apuesta['color'] != BLACK else WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

# Dibujar el cartón de apuestas
def draw_carton():
    for row in range(carton_filas):
        for col in range(carton_columnas):
            x = carton_pos[0] + col * carton_casilla_ancho
            y = carton_pos[1] + row * carton_casilla_alto
            pygame.draw.rect(screen, WHITE, (x, y, carton_casilla_ancho, carton_casilla_alto))
            pygame.draw.rect(screen, BLACK, (x, y, carton_casilla_ancho, carton_casilla_alto), 2)
            num = orden_tablero[row * carton_columnas + col]  # Obtener el número según orden_tablero
            font = pygame.font.SysFont("Arial", 18)
            label = font.render(str(num), True, BLACK)
            screen.blit(label, (x + (carton_casilla_ancho - label.get_width()) / 2, 
                                y + (carton_casilla_alto - label.get_height()) / 2))

# Función principal
def main():
    global screen, turno_actual
    add_chips_for_current_player()  # Cargar las fichas del primer jugador
    while True:
        screen.fill(DARK_GRAY)
        app_events()

        # Dibujar cartón y apuestas
        draw_carton()
        draw_apuestas()
        draw_chips()

        # Dibujar el botón de cambio de turno
        pygame.draw.rect(screen, BLUE, boton_rect)
        font = pygame.font.Font(None, 30)
        label = font.render('Cambiar Turno', True, WHITE)
        screen.blit(label, (boton_rect.x + (boton_rect.width - label.get_width()) / 2, 
                            boton_rect.y + (boton_rect.height - label.get_height()) / 2))

        pygame.display.flip()
        clock.tick(60)

# Ejecutar el juego
if __name__ == '__main__':
    main()
