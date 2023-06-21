from settings.settings import WIDTH, HEIGHT, TIME_BUTTONS, BLACK
import pygame
from math import acos, sqrt, degrees
import numpy as np
import json
import os
from collections import defaultdict

def get_mid(coord_a, coord_b, coord_c):
    return (coord_a + coord_b + coord_c) / 3


def escale_coor_pix(coor_x, coor_y, escale, offset_x=0, offset_y=0):

    x_pix = (coor_x * escale[0]) + offset_x
    y_pix = (coor_y * escale[1]) + offset_y
    return (x_pix, y_pix)

def distance_between_pixels(p1, p2):
    return abs(p2[0] - p1[0])

def create_list(data):
    if data != None:
        return [f"{i[0]}-{i[1]}" for i in data]
    else:
        return "No data exist"
def create_list_users(data):
    if data != None:
        return [f"{i[0]}-{i[1]}_{i[2]}" for i in data]
    else:
        return "No data exist"

def get_id(name):
    return name.split("-")[0]


def distribute_data(data):
    tiempo, tiempo_ejer, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos = (
        [],
        [],
        [],
        [],
        [],
        [],
    )

    for i in data:
        tiempo.append(i[0].strftime("%d/%m"))
        tiempo_ejer.append(i[1])
        izq_errores.append(i[2])
        izq_aciertos.append(i[3])
        drcha_errores.append(i[4])
        drcha_aciertos.append(i[5])
    
    return tiempo, tiempo_ejer, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos

def distribute_data_stats(data):
    fecha, errores, aciertos, tiempo = (
        [],
        [],
        [],
        [],
    )
    for i in data:
        fecha.append(i[0].strftime("%d/%m"))
        errores.append(i[2])
        aciertos.append(i[3])
        tiempo.append(i[1])

    return fecha, errores, aciertos, tiempo


def distribute_data_squad(data):
    fecha, errores, aciertos, media_angulo, tiempo = (
        [],
        [],
        [],
        [],
        [],
    )
    for i in data:
        fecha.append(i[0].strftime("%d/%m"))
        errores.append(i[2])
        aciertos.append(i[3])
        media_angulo.append(i[4])
        tiempo.append(i[1])

    return fecha, errores, aciertos, media_angulo, tiempo

def reset_time():
    return 0, 0


def count(start_ticks):
    seconds = (
        pygame.time.get_ticks() - start_ticks
    ) / 1000  # calculate how many seconds
    if seconds >= TIME_BUTTONS:
        return seconds
    return seconds

def cargar_archivos_folder(carpeta, scale):
    r_files = []
    files = sorted([file for file in os.listdir(carpeta)])
    for i in files:
        image = pygame.image.load(f"{carpeta}/{i}")
        image.set_colorkey(BLACK)
        scaled_image = pygame.transform.scale(image, scale)
        r_files.append(scaled_image)

    return r_files

def reset_pygame_timer():
    return pygame.time.get_ticks()

def get_str_time(min, sec):
    minutes = ''
    if len(str(min)) == 1:
        minutes = f'0{min}'
    else:
        minutes = f'{min}'
    segundos = ''
    if sec == 0:
        segundos = '00'
    elif len(str(sec)) == 1:
        segundos = f'0{sec}'
    elif len(str(sec)) == 2:
        segundos = f'{sec}'
    
    return f'{minutes}:{segundos}'

def get_vectors(p1,p2):
    return ((p2[0]-p1[0], p2[1]-p1[0]))


def angle_calculate_by_points(p1, p2, p3):

    p1 = np.array([p1[0], p1[1]])
    p2 = np.array([p2[0], p2[1]])
    p3 = np.array([p3[0], p3[1]])
    l1 = np.linalg.norm(p2 - p3)
    l2 = np.linalg.norm(p1 - p3)
    l3 = np.linalg.norm(p1 - p2)
    # Calcular el ángulo
    return degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))

def read(file, text):
    with open(file, 'r') as archivo:
        contenido = archivo.read()

    json_dict = json.loads(contenido)
    # Obtener el valor asociado a la clave especificada
    valor = json_dict.get(text)
    return valor

def new_json_value(file, key, nuevo_valor):
    with open(file, 'r') as archivo:
        contenido = archivo.read()
        
    json_dict = json.loads(contenido)

    json_dict[key] = nuevo_valor    
    with open(file, 'w') as archivo:
        archivo.write(json.dumps(json_dict))