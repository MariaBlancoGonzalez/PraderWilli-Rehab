from settings import WIDTH, HEIGHT, TIME_BUTTONS
import pygame


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
    if len(min) == 1:
        minutes = f'0{min}'
    else:
        minutes = f'{min}'
    segundos = ''
    if sec == 0:
        segundos = '00'
    elif len(sec) == 1:
        segundos = f'0{sec}'
    elif len(sec) == 2:
        segundos = f'{sec}'
    
    return f'{minutes}:{segundos}'