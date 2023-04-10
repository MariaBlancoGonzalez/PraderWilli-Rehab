from mediapipe.python.solutions import pose as mp_pose
import os
from settings import WIDTH, HEIGHT, BODY_PARTS

def get_mid(coord_a, coord_b, coord_c):
            return ((coord_a+coord_b+coord_c)/3)

def escale_coor_pix(coor_x, coor_y, offset_x = 0, offset_y = 0):
    x_pix = (coor_x * WIDTH) + offset_x
    y_pix = (coor_y * HEIGHT) + offset_y

    return (x_pix, y_pix)

def distance_between_pixels(p1, p2):
    return abs(p2[0]-p1[0])

def extract_face_landmarks(pose):
    body_landmarks = []

    for index in BODY_PARTS:
        body_landmarks.append(pose.pose_landmarks.landmark[index])
    
    return body_landmarks

def get_points(results):     
    # For each hand
    try:
        left_x = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x))

        left_y = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y))

        right_x = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x))

        right_y = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y))

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0,0), (0,0)
    
def get_feet_points(results):
    # For each hand
    try:
        left_x = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x)

        left_y = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y)

        right_x = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x)

        right_y = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y)

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)

def create_list(data):
    if data != None:
        return [f'{i[0]}-{i[1]}' for i in data]
    else:
        return 'No data exist'
    

def get_id(name):
    return name.split('-')[0]


# For statistics
def calculate_media_total(data1, data2):
    return sum(data1 + data2) / len(data1 + data2)

def get_best_score(data):
    new_datos = [[i[3], i[6]+i[8]] for i in data]
    max, date = 0, None
    for i in new_datos:
        if i[1] >= max:
            max = i[1]
            date = i[0]
    return max, date.strftime('%d/%m')

def calculate_media_parte(data):
    return sum(data)/len(data)


def distribute_data(data):
    tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos = [], [], [], [], []
    for i in data:
        tiempo.append(i[3].strftime('%d/%m'))
        izq_errores.append(i[5])
        izq_aciertos.append(i[6])
        drcha_errores.append(i[7])
        drcha_aciertos.append(i[8])

    return tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos
