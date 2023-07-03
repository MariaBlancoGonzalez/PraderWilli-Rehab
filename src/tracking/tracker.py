import cv2
import mediapipe as mp
from settings import settings as settings

class ObjectTracker:
    def __init__(self):
        self.__pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.results = None
        self.landmark_process = []

    def pose_tracking(self, frame):
        try:
            self.results = self.__pose.process(frame)
            self.convert_coordinates()
        except:
            pass

    def convert_coordinates(self):
        self.landmark_process.clear()
        for landmark in self.results.pose_landmarks.landmark:
            x = landmark.x * settings.WIDTH
            y = landmark.y * settings.HEIGHT
            visibility = landmark.visibility

            landmark_dict = {
                'x': x,
                'y': y,
                'visibility': visibility
            }
            self.landmark_process.append(landmark_dict)
