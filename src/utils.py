from settings import WIDTH, HEIGHT, TIME_BUTTONS
import pygame
from math import acos, sqrt, degrees
import numpy as np

def get_mid(coord_a, coord_b, coord_c):
    return (coord_a + coord_b + coord_c) / 3


def escale_coor_pix(coor_x, coor_y, offset_x=0, offset_y=0):
    x_pix = (coor_x * WIDTH) + offset_x
    y_pix = (coor_y * HEIGHT) + offset_y

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
    tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos = (
        [],
        [],
        [],
        [],
        [],
    )
    for i in data:
        tiempo.append(i[3].strftime("%d/%m"))
        izq_errores.append(i[5])
        izq_aciertos.append(i[6])
        drcha_errores.append(i[7])
        drcha_aciertos.append(i[8])

    return tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos


def distribute_data_stats(data):
    fecha, errores, aciertos, caidas, tiempo = (
        [],
        [],
        [],
        [],
        [],
    )
    for i in data:
        fecha.append(i[3].strftime("%d/%m"))
        errores.append(i[5])
        aciertos.append(i[6])
        caidas.append(i[7])
        tiempo.append(i[4])


    return fecha, errores, aciertos, caidas, tiempo


def distribute_data_squad(data):
    fecha, errores, aciertos, tiempo = (
        [],
        [],
        [],
        [],
    )
    for i in data:
        fecha.append(i[3].strftime("%d/%m"))
        errores.append(i[5])
        aciertos.append(i[6])
        tiempo.append(i[4])

    return fecha, errores, aciertos, tiempo



def reset_time():
    return 0, 0


def count(start_ticks):
    seconds = (
        pygame.time.get_ticks() - start_ticks
    ) / 1000  # calculate how many seconds
    if seconds >= TIME_BUTTONS:
        return seconds
    return seconds


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
    '''# left_current_hip, left_knee, left_current_foot
    v1 = get_vectors(p2,p1)
    v2 = get_vectors(p2,p3)
    #Calcula el producto punto de los vectores
    dot_product = v1[0]*v2[0] + v1[1]*v2[1]

    # Calcula la longitud de los vectores
    length_v1 = sqrt(v1[0]**2 + v1[1]**2)
    length_v2 = sqrt(v2[0]**2 + v2[1]**2)

    # Calcula el coseno del ángulo entre los vectores
    cos_angle = dot_product / (length_v1 * length_v2)

    # Calcula el ángulo en radianes y conviértelo a grados
    angle_rad = acos(cos_angle)
    angle_deg = degrees(angle_rad)

    # Devuelve el ángulo en grados
    return angle_deg
    
    return degrees(acos(p2p1_p2p3/(mod_p2p1*mod_p2p3)))'''
    radians = np.arctan2(p3[1] - p2[1], p3[0]-p2[0]) - \
        np.arctan2(p1[1]-p2[1], p1[0]-p2[0])
    angle = np.abs(radians*180.0/np.pi)
    return angle