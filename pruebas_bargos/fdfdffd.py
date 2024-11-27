import pygame
from surface_logic import *  # Importa todo lo que está en surface_logic.py

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 860
SCREEN_HEIGHT = 680

# Inicializar pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test Surface")

# Crear Surface grande
surface.fill((255, 255, 255))  # Puedes modificar la Surface importada aquí
close_button_rect = {
        "x": SCREEN_WIDTH - 60,
        "y": 10,
        "width": 50,
        "height": 25,
    }
# Botón Historial
historial_button_rect = {
    "x": 50,
    "y": 10,
    "width": 100,
    "height": 40,
}

# Función para dibujar el botón de historial
def draw_historial_button():
    pygame.draw.rect(screen, (0, 255, 0), (historial_button_rect["x"], historial_button_rect["y"], historial_button_rect["width"], historial_button_rect["height"]))
    font = pygame.font.SysFont("Arial", 20)
    text = font.render("Historial", True, BLACK)
    screen.blit(text, (historial_button_rect["x"] + 15, historial_button_rect["y"] + 10))

# Función para manejar el clic en el botón Historial
def handle_historial_button_click(mouse, show_surface):
    if is_point_in_rect(mouse, historial_button_rect):  # Verificar si se ha hecho clic en el botón
        show_surface = not show_surface  # Cambiar el estado de show_surface (True/False)
    return show_surface

# Bucle principal
def main():
    mouse = {"x": 0, "y": 0, "pressed": False}
    show_surface = False  # Inicialmente no mostrar la surface
    while True:
        mouse["x"], mouse["y"] = pygame.mouse.get_pos()

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse["pressed"] = True
                # Manejar clic en el botón Historial
                show_surface = handle_historial_button_click(mouse, show_surface)

        # Actualizar la posición del scroll
        update_scroll_position(mouse)

        # Dibujar la pantalla
        screen.fill((255, 255, 255))

        # Dibujar el botón Historial
        draw_historial_button()

        # Si show_surface es True, mostrar la surface
        if show_surface:
            draw_surface()  # Mostrar la Surface
            draw_scroll_slider()  # Dibujar el slider del scroll
            draw_close_button(close_button_rect)  # Botón de cierre
            print(show_surface)
            show_surface = events_surface(mouse,close_button_rect,show_surface)

            print(show_surface)
        pygame.display.update()  # Actualizar la pantalla

if __name__ == "__main__":
    main()
