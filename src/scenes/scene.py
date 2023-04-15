class Scene:
    def __init__(self, game):
        self.game = game
        self._name_scene = ''

    def get_name(self):
        return self._name_scene

    def events(self, events):
        raise NotImplementedError("events must be defined")

    def update(self, dt):
        raise NotImplementedError("update must be defined")

    def draw(self):
        raise NotImplementedError("draw must be defined")
