from mediapipe.python.solutions import pose as mp_pose
import os
import math
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

def euclidean_distance(p1, p2):
    return math.sqrt((p1)**2 + (p2)**2)

def create_diagonal_points_right(results):
    # FOR LEFT PART
    shoulder = escale_coor_pix(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                               results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
    elbow = escale_coor_pix(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y)
    hand = get_points_left(results)
    hand = escale_coor_pix(hand[0], hand[1])
   
    # PIXEL VECTOR
    shoulder_to_elbow = (elbow[0] - shoulder[0],
                         elbow[1] - shoulder[1])
    
    shoulder_elbow_segment = euclidean_distance(shoulder_to_elbow[0], shoulder_to_elbow[1])

    elbow_to_hand = (hand[0] - elbow[0], hand[1] - elbow[1])
    elbow_hand_segment = euclidean_distance(elbow_to_hand[0], elbow_to_hand[1])
    # Multiplica el vector del codo a la mano por la longitud del vector del hombro al codo
    hand_pos = (shoulder[0] + (elbow_hand_segment+shoulder_elbow_segment),
                shoulder[1])

    return hand_pos


def create_diagonal_points_left(results):
    # FOR LEFT PART
    shoulder = escale_coor_pix(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                               results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y)
    elbow = escale_coor_pix(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
                            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y)
    hand = get_points_right(results) 
    hand = escale_coor_pix(hand[0], hand[1])
 
    # PIXEL VECTOR
    shoulder_to_elbow = (elbow[0] - shoulder[0],
                         elbow[1] - shoulder[1])

    shoulder_elbow_segment = euclidean_distance(
        shoulder_to_elbow[0], shoulder_to_elbow[1])

    elbow_to_hand = (hand[0] - elbow[0], hand[1] - elbow[1])
    elbow_hand_segment = euclidean_distance(elbow_to_hand[0], elbow_to_hand[1])
    # Multiplica el vector del codo a la mano por la longitud del vector del hombro al codo
    hand_pos = (shoulder[0] - (elbow_hand_segment+shoulder_elbow_segment),
                shoulder[1])

    return hand_pos

def get_points_left(results):
    # For each hand
    try:
        left_x = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x),
                         float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].x),
                         float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x))

        left_y = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y),
                         float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].y),
                         float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y))

        # Coordinates
        return (left_x, left_y)

    except:
        return (0, 0)
    
def get_points_right(results):
    # For each hand
    try:
        right_x = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x),
                          float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].x),
                          float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x))

        right_y = get_mid(float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y),
                          float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].y),
                          float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y))

        # Coordinates
        return (right_x, right_y)

    except:
        return (0, 0)

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
    

def get_shoulder_pos(results):
    try:
        shoulder_left = (escale_coor_pix(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y))

        shoulder_right = (escale_coor_pix(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y))
        
        return shoulder_left, shoulder_right
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
