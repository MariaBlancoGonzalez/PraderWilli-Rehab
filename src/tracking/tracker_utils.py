from pygame.sprite import Group
import math

from utils import *
from settings.settings import BODY_PARTS

from mediapipe.python.solutions import pose as mp_pose


def extract_face_landmarks(pose):
    body_landmarks = []

    for index in BODY_PARTS:
        body_landmarks.append(pose.pose_landmarks.landmark[index])

    return body_landmarks


def euclidean_distance(p1, p2):
    return math.sqrt((p1) ** 2 + (p2) ** 2)


def create_diagonal_points_right(pose):
    # FOR LEFT PART
    shoulder = (pose[11]['x'],pose[11]['y'])
    elbow = (pose[13]['x'],pose[13]['y'])

    hand, _ = get_hands_points(pose)

    # PIXEL VECTOR
    shoulder_to_elbow = (elbow[0] - shoulder[0], elbow[1] - shoulder[1])

    shoulder_elbow_segment = euclidean_distance(
        shoulder_to_elbow[0], shoulder_to_elbow[1]
    )

    elbow_to_hand = (hand[0] - elbow[0], hand[1] - elbow[1])
    elbow_hand_segment = euclidean_distance(elbow_to_hand[0], elbow_to_hand[1])
    # Multiplica el vector del codo a la mano por la longitud del vector del hombro al codo
    hand_pos = (
        shoulder[0] + (elbow_hand_segment + shoulder_elbow_segment),
        shoulder[1],
    )

    return hand_pos


def create_diagonal_points_left(pose):
    # FOR RIGHT PART
    shoulder = (pose[12]['x'],pose[12]['y'])
    elbow = (pose[14]['x'], pose[14]['y'])
    _ , hand = get_hands_points(pose)

    # PIXEL VECTOR
    shoulder_to_elbow = (elbow[0] - shoulder[0], elbow[1] - shoulder[1])

    shoulder_elbow_segment = euclidean_distance(
        shoulder_to_elbow[0], shoulder_to_elbow[1]
    )

    elbow_to_hand = (hand[0] - elbow[0], hand[1] - elbow[1])
    elbow_hand_segment = euclidean_distance(elbow_to_hand[0], elbow_to_hand[1])
    # Multiplica el vector del codo a la mano por la longitud del vector del hombro al codo
    hand_pos = (
        shoulder[0] - (elbow_hand_segment + shoulder_elbow_segment),
        shoulder[1],
    )

    return hand_pos

def create_top_margin(pose):
    # FOR RIGHT PART
    shoulder = (pose[11]['x'],pose[11]['y'])
    elbow = (pose[13]['x'],pose[13]['y'])

    hand, _ = get_hands_points(pose)

    # PIXEL VECTOR
    shoulder_to_elbow = (elbow[0] - shoulder[0], elbow[1] - shoulder[1])

    shoulder_elbow_segment = euclidean_distance(
        shoulder_to_elbow[0], shoulder_to_elbow[1]
    )

    elbow_to_hand = (hand[0] - elbow[0], hand[1] - elbow[1])
    elbow_hand_segment = euclidean_distance(elbow_to_hand[0], elbow_to_hand[1])
    # Multiplica el vector del codo a la mano por la longitud del vector del hombro al codo
    margin_point = (
        shoulder[0],
        shoulder[1] -  (elbow_hand_segment + shoulder_elbow_segment),
    )

    return margin_point

def get_hands_points(pose):
    # For each hand
    try:
        right_x = get_mid(pose[15]['x'],pose[17]['x'],pose[19]['x'])
        right_y = get_mid(pose[15]['y'],pose[17]['y'],pose[19]['y'])

        left_x = get_mid(pose[16]['x'],pose[18]['x'],pose[20]['x'])
        left_y = get_mid(pose[16]['y'],pose[18]['y'],pose[20]['y'])

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)


def get_shoulder_pos(pose):
    try:
        shoulder_left =(pose[11]['x'],pose[11]['y'])
        shoulder_right = (pose[12]['x'],pose[12]['y'])

        return shoulder_left, shoulder_right
    except:
        return (0, 0), (0, 0)


def get_feet_points(pose):
    # For each hand
    try:
        right_x = pose[27]['x']
        right_y = pose[27]['y']

        left_x = pose[28]['x']
        left_y = pose[28]['y']

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)

def get_head_points(pose):
    # For each hand
    try:

        nose_x = pose[0]['x']
        nose_y = pose[1]['y']

        # Coordinates
        return (nose_x, nose_y)

    except:
        return (0, 0)

def check_collide(part, left, right, part_str=""):
    if part.top_rect.collidepoint(
        left.rect.centerx, left.rect.centery
    ) or part.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
        return part_str
    return ""


def check_visibility(pose):
    try:
        visibility = [i['visibility'] for i in pose]
        return all(i >= 0.55 for i in visibility)
    except:
        return False


def check_visibility_squad(pose):
    try:
        
        ankle = float(pose[27]['visibility'])
        shoulder = float(pose[11]['visibility'])
        hip = float(pose[23]['visibility'])
        knee = float(pose[25]['visibility'])

        visib = [ankle, shoulder, hip, knee]
        # Coordinates
        return all(i >= 0.65 for i in visib)

    except:
        return False


def check_visibility_balls(pose):
    try:
        visibility = [i['visibility'] for i in pose]
        return all(i >= 0.5 for i in visibility)
    except:
        return False
        
def get_knees_points(pose):
    # For each hand
    try:
        right_x = float(pose[25]['x'])
        right_y = float(pose[25]['y'])

        left_x = float(pose[26]['x'])
        left_y = float(pose[26]['y'])

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)


def get_hips_points(pose):
    # For each hand
    try:
        right_x = float(pose[23]['x'])
        right_y = float(pose[23]['y'])

        left_x = float(pose[24]['x'])
        left_y = float(pose[24]['y'])

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)

def update_pose_points(pose):
    pose_group = Group()
    try:
        for landmark in pose:
            # Convertir las coordenadas normalizadas a las coordenadas de la imagen
            x = int(landmark['x'])
            y = int(landmark['y'])

            # Crear un sprite para cada punto de la pose y agregarlo al grupo
            pose_point = pygame.sprite.Sprite()
            pose_point.rect = pygame.Rect(x, y, 5, 5)  # Tamaño del punto
            pose_point.image = pygame.Surface(pose_point.rect.size)
                
            pose_point.image.fill((255, 0, 0))
            pose_point.rect.center = (x, y)
            pose_group.add(pose_point)
        return pose_group
    except:
        return pose_group

