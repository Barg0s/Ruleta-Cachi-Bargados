import pygame
import sys
BLUE = (50, 120, 200)
WHITE = (255,255,255)

def mostrar_guanyadors(screen,seleccionado,historial):
    dibuixar_mini_log(screen)
    font = pygame.font.SysFont("Arial",17)

    # Actualizar la pantalla
    if seleccionado is not None:
        x = 650
        y = 100
        for num in historial: 
            texto_seleccion = font.render(f"Ha sortit:{num}", True, (0,0,0))
            screen.blit(texto_seleccion, (x - texto_seleccion.get_width() // 2, y))
            y += 20


def gestionar_nums(historial,num):
    historial.append(num)
    if len(historial) > 7:
        historial.pop(0)



def dibuixar_mini_log(screen):
    font = pygame.font.SysFont("Arial",17)
    pygame.draw.rect(screen, WHITE, (600, 50, 200, 200))
    txt = font.render("ULTIMS NUMEROS",True,WHITE)
    pygame.draw.rect(screen, BLUE, (600, 50, 200, 50))
    screen.blit(txt, (600 + (200 - txt.get_width()) // 2, 60))
    pygame.draw.rect(screen, (0,0,0), (600, 50, 200, 50),5)





def afegir_accio(historial,accio):
    historial.append(accio)