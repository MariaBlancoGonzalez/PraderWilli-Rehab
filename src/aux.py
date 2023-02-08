from mediapipe.python.solutions import pose as mp_pose
import os

def get_mid(coord_a, coord_b, coord_c):
            return ((coord_a+coord_b+coord_c)/3)

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
