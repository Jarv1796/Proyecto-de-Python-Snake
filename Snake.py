#!/usr/bin/env python3
"""
Estudiante: José Andrés Rodríguez Vásquez B46007.
Esta es una versión del videojuego Snake creada en Python y con
ayuda de la biblioteca PyGame. Se verificó que el código 
cumpliera con PEP-8 con la herramienta flake8.
"""
import pygame
import sys
import subprocess

# Definir los colores (personalizados con paletton.com)
BLANCO = (235, 235, 235)
CYAN = (0, 146, 140)

# Definir las dimensiones de la ventana
ANCHO = 800
ALTO = 600


# Función para reproducir la música de fondo
def reproducir_musica():
    pygame.mixer.init()  # Inicializar el mixer
    pygame.mixer.music.load("arcade_menu.mp3")  # Cargar la canción del menú
    pygame.mixer.music.play(-1)  # Reproducir en bucle


# Cargar efectos de sonido
def cargar_efectos_sonido():
    # Cargar el efecto de sonido
    pygame.mixer.init()  # Inicializar el mixer
    pygame.mixer.music.load("click.mp3")
    return {  # Puede utilizarse fácilmente después
        "clic": pygame.mixer.Sound("click.mp3")
    }


# Función para mostrar el menú principal
def mostrar_menu(efectos_sonido):  # Cargando efectos de sonido
    pygame.init()  # Inicializar Pygame
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Snake - Menú Principal")
    clock = pygame.time.Clock()

    # Cargar el fondo del menú
    fondo = pygame.image.load("fondo_menu.jpg").convert()

    # Mostrar las opciones del menú
    fuente = pygame.font.Font(None, 36)
    opcion_jugar = fuente.render("Jugar", True, BLANCO)
    opcion_dificultad = fuente.render("Dificultad", True, BLANCO)
    opcion_controles = fuente.render("Controles", True, BLANCO)
    opcion_salir = fuente.render("Salir", True, BLANCO)

    # Dificultad fácil por defecto
    dificultad_seleccionada = "Fácil"

    # Lógica del menú
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana 'X'
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Al clickear
                x, y = pygame.mouse.get_pos()
                if 300 <= x <= 500 and 200 <= y <= 250:
                    # Opción Jugar
                    efectos_sonido["clic"].play()  # Reproduce efecto
                    # Abre el juego en la dificultad seleccionada
                    jugar_nivel(dificultad_seleccionada)
                elif 300 <= x <= 500 and 300 <= y <= 350:
                    # Opción Dificultad
                    efectos_sonido["clic"].play()
                    # Abre el submenú de dificultad
                    dificultad_seleccionada = seleccionar_dificultad(
                        dificultad_seleccionada
                    )
                elif 300 <= x <= 500 and 400 <= y <= 450:
                    # Abre el submenú de controles
                    efectos_sonido["clic"].play()
                    mostrar_controles()
                elif 300 <= x <= 500 and 500 <= y <= 550:
                    # Salir del juego
                    efectos_sonido["clic"].play()
                    pygame.quit()
                    sys.exit()

        # Mostrar las opciones en (x,y) posición
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(opcion_jugar, (300, 200))
        pantalla.blit(opcion_dificultad, (300, 300))
        pantalla.blit(opcion_controles, (300, 400))
        pantalla.blit(opcion_salir, (300, 500))
        # Muestra en pantalla la dificultad actual
        mostrar_texto_dificultad(pantalla, dificultad_seleccionada, fuente)

        pygame.display.flip()
        clock.tick(30)


# Función para mostrar el texto de la dificultad
def mostrar_texto_dificultad(pantalla, dificultad_seleccionada, fuente):
    # Crear el texto de dificultad actual (color cyan)
    texto_dificultad = fuente.render(
        f"Dificultad: {dificultad_seleccionada}", True, CYAN
    )
    pantalla.blit(texto_dificultad, (450, 50))  # Mostrar texto en (x,y) posición


# Función para jugar
def jugar_nivel(dificultad):
    # Se define el archivo del juego
    archivo = "game.py"

    # Cerrar la ventana del menú
    pygame.quit()

    # Ejecutar el juego en la dificultad seleccionada (como argumento)
    subprocess.run(["python", archivo, dificultad])

    # Una vez finalizado el juego
    # Volver a abrir el menú principal
    reproducir_musica()
    mostrar_menu(efectos_sonido)


# Función para el submenú de dificultad
def seleccionar_dificultad(dificultad_actual):
    # Inicia la ventana del submenú
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake - Seleccionar Dificultad")
    clock = pygame.time.Clock()

    # Carga el fondo del submenú
    fondo = pygame.image.load("fondo_menu.jpg").convert()

    # Mostrar las opciones del submenú
    fuente = pygame.font.Font(None, 36)
    opcion_facil = fuente.render("Fácil", True, BLANCO)
    opcion_intermedio = fuente.render("Intermedio", True, BLANCO)
    opcion_dificil = fuente.render("Difícil", True, BLANCO)
    opcion_volver = fuente.render("Volver", True, BLANCO)

    # Obtiene la dificultad seleccionada previamente
    dificultad_seleccionada = dificultad_actual

    # Lógica del submenú
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana 'X'
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Al clickear
                x, y = pygame.mouse.get_pos()
                if 300 <= x <= 500 and 200 <= y <= 250:
                    # Opción Fácil
                    efectos_sonido["clic"].play()  # Reproducir efecto de sonido
                    # Cambiar la dificultad a fácil
                    dificultad_seleccionada = "Fácil"
                elif 300 <= x <= 500 and 300 <= y <= 350:
                    # Opción Intermedio
                    efectos_sonido["clic"].play()
                    # Cambiar la dificultad a intermedio
                    dificultad_seleccionada = "Intermedio"
                elif 300 <= x <= 500 and 400 <= y <= 450:
                    # Opción Difícil
                    efectos_sonido["clic"].play()
                    # Cambiar la dificultad a difícil
                    dificultad_seleccionada = "Difícil"
                elif 600 <= x <= 700 and 500 <= y <= 550:
                    # Opción Volver
                    efectos_sonido["clic"].play()
                    # Devuelve la dificultad seleccionada
                    return dificultad_seleccionada

        # Mostrar las opciones en (x,y) posición
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(opcion_facil, (300, 200))
        pantalla.blit(opcion_intermedio, (300, 300))
        pantalla.blit(opcion_dificil, (300, 400))
        pantalla.blit(opcion_volver, (600, 500))
        # Mostrar el texto de dificultad seleccionada
        mostrar_texto_dificultad(pantalla, dificultad_seleccionada, fuente)

        pygame.display.flip()
        clock.tick(30)


# Función para mostrar los controles
def mostrar_controles():
    # Inicia la ventana del submenú
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake - Controles")
    clock = pygame.time.Clock()

    # Cargar el fondo del submenú
    fondo = pygame.image.load("fondo_menu.jpg").convert()

    # Textos del submenú y opción volver
    fuente = pygame.font.Font(None, 36)
    texto_controles = fuente.render("Controles:", True, BLANCO)
    texto_flechas = fuente.render(
        "Utiliza ↑↓←→ para mover a la serpiente.", True, BLANCO
    )
    texto_pausa = fuente.render("Presiona ESPACIO para pausar el juego.", True, BLANCO)
    opcion_volver = fuente.render("Volver", True, BLANCO)

    # Lógica del submenú
    while True:
        for event in pygame.event.get():  # Al cerrar la ventana 'X'
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Al clickear
                x, y = pygame.mouse.get_pos()
                if 600 <= x <= 700 and 500 <= y <= 550:
                    # Opción Volver
                    efectos_sonido["clic"].play()
                    # Volver (literalmente)
                    return

        # Mostrar los textos y opción volver en pantalla
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(texto_controles, (200, 200))
        pantalla.blit(texto_flechas, (200, 300))
        pantalla.blit(texto_pausa, (200, 400))
        pantalla.blit(opcion_volver, (600, 500))
        mostrar_texto_dificultad(pantalla, "Fácil", fuente)

        pygame.display.flip()
        clock.tick(30)


##### Al abrir el menú
# Cargar efectos de sonido
efectos_sonido = cargar_efectos_sonido()

# Reproducir música de fondo
reproducir_musica()

# Llamar a la función para mostrar el menú principal
mostrar_menu(efectos_sonido)  # Con efectos de sonido
#####
