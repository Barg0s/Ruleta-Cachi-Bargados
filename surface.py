import pygame
import sys
import utils
# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (150, 150, 150)

# Dimensiones de la pantalla
SCREEN_WIDTH = 860
SCREEN_HEIGHT = 680

# Inicializar pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scroll Test")

# Crear Surface grande
surface = pygame.Surface((SCREEN_WIDTH, 1500)) 
surface.fill(WHITE)

# Dibujar contenido en la Surface
font = pygame.font.SysFont("Arial", 15)
def dibuixar_historial(historial):
    y = 100
    for accio in (historial):
        text = font.render(accio,True,BLACK)
        surface.blit(text,(50,y))
        y += 25

# Configuración del scroll
scroll = {
    "x": SCREEN_WIDTH - 20,  
    "y": 50,
    "width": 10,
    "height": 600,  
    "radius": 10,
    "percentage": 0,  
    "dragging": False,
    "surface_offset": 0, 
}

def generar_cerrar():
    close_button_rect = {
        "x": SCREEN_WIDTH - 60,
        "y": 10,
        "width": 50,
        "height": 25,
    }
    return close_button_rect


# Dibujar el scroll y su círculo
def draw_scroll_slider():
    pygame.draw.rect(screen, GRAY, (scroll["x"], scroll["y"], scroll["width"], scroll["height"]))
    circle_x = scroll["x"] + scroll["width"] // 2
    max_scroll_y = scroll["y"] + scroll["height"] - scroll["radius"]
    min_scroll_y = scroll["y"] + scroll["radius"]
    circle_y = int(min_scroll_y + (scroll["percentage"] / 100) * (max_scroll_y - min_scroll_y))
    pygame.draw.circle(screen, BLACK, (circle_x, circle_y), scroll["radius"])

# Actualizar la posición del scroll
def update_scroll_position(mouse):
    if scroll["dragging"]:
        max_scroll_y = scroll["y"] + scroll["height"] - scroll["radius"]
        min_scroll_y = scroll["y"] + scroll["radius"]
        relative_y = max(min(mouse["y"], max_scroll_y), min_scroll_y)
        
        # Actualiza el porcentaje basado en la posición del mouse
        scroll["percentage"] = ((relative_y - min_scroll_y) / (max_scroll_y - min_scroll_y)) * 100

    # Calcula el desplazamiento proporcional
    max_offset = surface.get_height() - SCREEN_HEIGHT
    scroll["surface_offset"] = int((scroll["percentage"] / 100) * max_offset)


# Dibujar el contenido desplazable
def draw_surface():
    sub_surface = surface.subsurface((0, scroll["surface_offset"], SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(sub_surface, (0, 0))


# Dibujar el botón de cierre
def draw_close_button(close_button_rect):
    pygame.draw.rect(screen, RED, (close_button_rect["x"], close_button_rect["y"], close_button_rect["width"], close_button_rect["height"]))
    text = pygame.font.SysFont("Arial", 20).render("X", True, BLACK)
    screen.blit(text, (close_button_rect["x"] + 15, close_button_rect["y"] + 5))




def events_surface(mouse, close_button_rect, show_surface):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse["pressed"] = True
            # Detectar clic en el botón de cierre (X)
            if utils.is_point_in_rect(mouse, close_button_rect):
                show_surface = False 
            else:
                circle_x = scroll["x"] + scroll["width"] // 2
                max_scroll_y = scroll["y"] + scroll["height"] - scroll["radius"]
                min_scroll_y = scroll["y"] + scroll["radius"]
                circle_y = int(min_scroll_y + (scroll["percentage"] / 100) * (max_scroll_y - min_scroll_y))
                
                if utils.is_point_in_circle(mouse, {"x": circle_x, "y": circle_y}, scroll["radius"]):
                    scroll["dragging"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse["pressed"] = False
            scroll["dragging"] = False

    return show_surface


