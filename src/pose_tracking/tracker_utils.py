from pygame.sprite import Group
import math

from utils import *
from settings import BODY_PARTS

from mediapipe.python.solutions import pose as mp_pose


def extract_face_landmarks(pose):
    body_landmarks = []

    for index in BODY_PARTS:
        body_landmarks.append(pose.pose_landmarks.landmark[index])

    return body_landmarks


def euclidean_distance(p1, p2):
    return math.sqrt((p1) ** 2 + (p2) ** 2)


def create_diagonal_points_right(results):
    # FOR LEFT PART
    shoulder = escale_coor_pix(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
    )
    elbow = escale_coor_pix(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y,
    )
    hand = get_points_left(results)
    hand = escale_coor_pix(hand[0], hand[1])

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


def create_diagonal_points_left(results):
    # FOR RIGHT PART
    shoulder = escale_coor_pix(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
    )
    elbow = escale_coor_pix(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y,
    )
    hand = get_points_right(results)
    hand = escale_coor_pix(hand[0], hand[1])

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

def create_top_margin(results):
    # FOR RIGHT PART
    shoulder = escale_coor_pix(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
    )
    elbow = escale_coor_pix(
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y,
    )
    hand = get_points_right(results)
    hand = escale_coor_pix(hand[0], hand[1])

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


def get_points_left(results):
    # For each hand
    try:
        left_x = get_mid(
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x),
        )

        left_y = get_mid(
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y),
        )

        # Coordinates
        return (left_x, left_y)

    except:
        return (0, 0)


def get_points_right(results):
    # For each hand
    try:
        right_x = get_mid(
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x),
        )

        right_y = get_mid(
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y),
        )

        # Coordinates
        return (right_x, right_y)

    except:
        return (0, 0)


def get_points(results):
    # For each hand
    try:
        right_x = get_mid(
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x),
        )

        right_y = get_mid(
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y),
        )

        left_x = get_mid(
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].x),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x),
        )

        left_y = get_mid(
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].y),
            float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y),
        )

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)


def get_shoulder_pos(results):
    try:
        shoulder_left = escale_coor_pix(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
        )

        shoulder_right = escale_coor_pix(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
        )

        return shoulder_left, shoulder_right
    except:
        return (0, 0), (0, 0)


def get_feet_points(results):
    # For each hand
    try:
        right_x = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x
        )

        right_y = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y
        )

        left_x = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x
        )

        left_y = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y
        )

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)


def check_collide(part, left, right, part_str=""):
    if part.top_rect.collidepoint(
        left.rect.centerx, left.rect.centery
    ) or part.top_rect.collidepoint(right.rect.centerx, right.rect.centery):
        return part_str
    return ""


def check_visibility(results):
    try:
        visibility = [i.visibility for i in results.pose_landmarks.landmark]
        return all(i >= 0.55 for i in visibility)
    except:
        return False


def check_visibility_squad(results):
    try:
        
        ankle = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].visibility
        )


        shoulder = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].visibility
        )

        hip = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].visibility
        )

        knee = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].visibility
        )
        visib = [ankle, shoulder, hip, knee]
        # Coordinates
        return all(i >= 0.65 for i in visib)

    except:
        return False


def check_visibility_balls(results):
    try:
        visibility = [i.visibility for i in results.pose_landmarks.landmark]
        return all(i >= 0.5 for i in visibility)
    except:
        return False
        
def get_knees_points(results):
    # For each hand
    try:
        right_x = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x)
            

        right_y = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y)

        left_x = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x)
        
        left_y = float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y)

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)


def get_hips_points(results):
    # For each hand
    try:
        right_x = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x)

        right_y = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y)

        left_x = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x)

        left_y = float(
            results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y)

        # Coordinates
        return (left_x, left_y), (right_x, right_y)

    except:
        return (0, 0), (0, 0)


def get_part_forward(results):
    return 'left' if float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].z) < float(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].z) else 'right'

from settings import WIDTH
from settings import HEIGHT
def update_pose_points(results):
    pose_group = Group()
    try:
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                # Convertir las coordenadas normalizadas a las coordenadas de la imagen
                x = int(landmark.x * WIDTH)
                y = int(landmark.y * HEIGHT)

                # Crear un sprite para cada punto de la pose y agregarlo al grupo
                pose_point = pygame.sprite.Sprite()
                pose_point.rect = pygame.Rect(x, y, 5, 5)  # Tamaño del punto
                pose_point.image = pygame.Surface(pose_point.rect.size)
                # Color del punto (rojo en este caso)
                pose_point.image.fill((255, 0, 0))
                pose_point.rect.center = (x, y)
                pose_group.add(pose_point)
        return pose_group
    except:
        return pose_group

