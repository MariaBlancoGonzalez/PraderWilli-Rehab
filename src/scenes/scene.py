from tracking.tracker import ObjectTracker

class Scene:
    def __init__(self, game):
        self.game = game
        self._name_scene = ""
        self.pose_tracker = ObjectTracker()
    def get_name(self):
        return self._name_scene

    def events(self, events=None):
        raise NotImplementedError("events must be defined")

    def render(self):
        raise NotImplementedError("draw must be defined")

    def update(self, frame):
        raise NotImplementedError("tracking body pose method must be implemented")
