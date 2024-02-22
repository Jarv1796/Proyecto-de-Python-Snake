#!/usr/bin/env python3
"""
Estudiante: José Andrés Rodríguez Vásquez B46007.
Esta es una versión del videojuego Snake creada en Python y con
ayuda de la biblioteca PyGame. Se verificó que el código 
cumpliera con PEP-8 con la herramienta flake8.
"""
# Se importan las bibliotecas
import pygame
import random
import time
import sys

# Inicializar Pygame
pygame.init()

# Definir los colores (personalizados con paletton.com)
NEGRO = (23, 37, 37)
BLANCO = (235, 235, 235)
NARANJA = (255, 61, 0)
VERDE = (4, 221, 4)

# Definir las dimensiones de la ventana
ANCHO = 800
ALTO = 600

# Definir el tamaño del bloque
TAM_BLOQUE = 20

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake")

# Cargar los efectos de sonido
sonido_comer = pygame.mixer.Sound("comida.mp3")
sonido_chocar = pygame.mixer.Sound("choque.mp3")


########## Función principal del juego
def juego():
    # Obtener la dificultad (desde el menú)
    dificultad = sys.argv[1]

    # Configuración según la dificultad
    VELOCIDAD = configurar_dificultad(dificultad)

    # Inicializar variables del juego
    juego_terminado = False
    pausa = False
    score = 0
    highscore = obtener_highscore()  # Obtener el highscore guardado
    reloj = pygame.time.Clock()

    # Coordenadas iniciales de la serpiente
    serpiente = [(ANCHO / 2, ALTO / 2)]
    direccion = "arriba"  # Hacia arriba por default

    # Generar posición inicial de la comida
    comida = generar_comida()

    # Bucle principal del juego
    while not juego_terminado:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Cerrar ventana desde la 'X'
                juego_terminado = True
            elif event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_UP and direccion != "abajo"
                ):  # Presionar la flecha abajo
                    direccion = "arriba"
                elif (
                    event.key == pygame.K_DOWN and direccion != "arriba"
                ):  # Presionar la flecha arriba
                    direccion = "abajo"
                elif (
                    event.key == pygame.K_LEFT and direccion != "derecha"
                ):  # Presionar la flecha derecha
                    direccion = "izquierda"
                elif (
                    event.key == pygame.K_RIGHT and direccion != "izquierda"
                ):  # Presionar la flecha izquierda
                    direccion = "derecha"
                elif event.key == pygame.K_SPACE:  # Pausar con la tecla espacio
                    pausa = not pausa

        # Pausa del juego
        if pausa:
            continue

        # Movimiento de la serpiente
        cabeza_x, cabeza_y = serpiente[0]
        if direccion == "derecha":
            cabeza_x += TAM_BLOQUE  # Aumenta coordenada x
        elif direccion == "izquierda":
            cabeza_x -= TAM_BLOQUE  # Disminuye coordenada x
        elif direccion == "arriba":
            cabeza_y -= TAM_BLOQUE  # Disminuye coordenada y
        elif direccion == "abajo":
            cabeza_y += TAM_BLOQUE  # Aumenta coordenada y

        # Verificar colisiones con los bordes
        if cabeza_x < 0 or cabeza_x >= ANCHO or cabeza_y < 0 or cabeza_y >= ALTO:
            juego_terminado = True  # Termina el juego
            sonido_chocar.play()  # Reproducir efecto de sonido al chocar

        # Verificar colisiones con la serpiente
        if (cabeza_x, cabeza_y) in serpiente[1:]:
            juego_terminado = True  # Termina el juego
            sonido_chocar.play()  # Reproducir efecto de sonido al chocar

        # Añadir nuevo bloque de cuerpo a la serpiente
        serpiente.insert(0, (cabeza_x, cabeza_y))

        # Cuando la serpiente come
        if cabeza_x == comida[0] and cabeza_y == comida[1]:
            comida = generar_comida()  # Se genera comida nuevamente
            score += 10  # Incrementa el score
            sonido_comer.play()  # Reproducir efecto de sonido al comer
            VELOCIDAD += 1  # Aumentar la velocidad cuando la serpiente come
            if score > highscore:  # Actualizar el highscore si es necesario
                highscore = score
                guardar_highscore(
                    highscore
                )  # Guardar el nuevo highscore si es necesario
        else:
            serpiente.pop()

        # Dibujar el fondo
        ventana.fill(NEGRO)

        # Dibujar la serpiente
        for segmento in serpiente:
            pygame.draw.rect(
                ventana, VERDE, (segmento[0], segmento[1], TAM_BLOQUE, TAM_BLOQUE)
            )

        # Dibujar la comida
        pygame.draw.rect(
            ventana, NARANJA, (comida[0], comida[1], TAM_BLOQUE, TAM_BLOQUE)
        )

        # Mostrar el score y el highscore en la pantalla
        mostrar_puntuacion(score, highscore)

        # Actualizar la pantalla
        pygame.display.update()

        # Controlar la velocidad del juego
        reloj.tick(VELOCIDAD)

    # Cuando termina el juego (juego_terminado = True)
    # Mostrar el score al perder
    mostrar_score_al_perder(score)

    # Esperar 2 segundos antes de cerrar la ventana
    time.sleep(2)

    # Cerrar el juego (Pygame)
    pygame.quit()


########## Función principal del juego


# Función para generar comida en una posición aleatoria
def generar_comida():
    comida_x = random.randrange(0, ANCHO, TAM_BLOQUE)
    comida_y = random.randrange(0, ALTO, TAM_BLOQUE)
    return (comida_x, comida_y)


# Función para mostrar la puntuación en la pantalla
def mostrar_puntuacion(score, highscore):
    fuente = pygame.font.SysFont(None, 24)
    texto_score = fuente.render(
        f"Score: {score}", True, BLANCO
    )  # Texto en color blanco
    texto_highscore = fuente.render(
        f"Highscore: {highscore}", True, BLANCO
    )  # Texto en color blanco
    ventana.blit(texto_score, (10, 10))  # Mostrar el texto
    ventana.blit(texto_highscore, (10, 30))  # Mostrar el texto


# Función para mostrar el score al perder
def mostrar_score_al_perder(score):
    fuente = pygame.font.SysFont(None, 40)
    texto_score = fuente.render(f"Score: {score}", True, BLANCO)
    ventana.blit(
        texto_score, (ANCHO // 2 - 50, ALTO // 2)
    )  # Mostrar el texto en el centro de la pantalla
    pygame.display.update()


# Función para obtener el highscore guardado
def obtener_highscore():
    try:
        with open("highscore.txt", "r") as archivo:  # Archivo para guardar el highscore
            highscore = int(archivo.read())  # Leer el archivo y pasar a entero
    except FileNotFoundError:  # En caso de error (archivo dañado o inexistente)
        highscore = 0
    return highscore


# Función para guardar el highscore
def guardar_highscore(highscore):
    with open("highscore.txt", "w") as archivo:  # Abre el archivo
        archivo.write(str(highscore))  # Escribe el highscore como cadena


# Función para configurar dificultad
def configurar_dificultad(dificultad):
    # Si la dificultad es 'Fácil'
    if dificultad == "Fácil":
        # Cargar la canción para la dificultad fácil
        pygame.mixer.music.load("arcade.mp3")
        # Velocidad en fácil
        velocidad = 5
    # Si la dificultad es 'Intermedio'
    elif dificultad == "Intermedio":
        # Cargar la canción para la dificultad intermedio
        pygame.mixer.music.load("rock.mp3")
        # Velocidad en intermedio
        velocidad = 8
    # Si la dificultad es 'Difícil'
    elif dificultad == "Difícil":
        # Cargar la canción para la dificultad difícil
        pygame.mixer.music.load("rock2.mp3")
        # Velocidad en difícil
        velocidad = 12
    # En caso de error
    else:
        raise ValueError("Dificultad no válida")

    # Reproducir la canción en bucle
    pygame.mixer.music.play(-1)
    # Devuelve la velocidad asociada a la dificultad
    return velocidad


# Llamado a la función principal del juego
juego()
