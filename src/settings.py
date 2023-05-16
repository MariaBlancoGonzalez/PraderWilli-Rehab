import pygame

# Texts
CAPTION = "Prader Willi"

# If not db
JSON_FILE = 'default.json'

# Cursor
CURSOR_CLICK = "./assets/icons/cursor_click.png"

# Tutorial
HISTORIAL = "./assets/images/historial.png"
OPCIONES = "./assets/images/opciones.png"

# Images and icons
ROCKET = "./assets/icons/cohete.png"
HAND_POINTER = "./assets/icons/hand-pointer.png"
ESTRELLA = "./assets/icons/estrella.png"
ROJO = "./assets/icons/rojo.png"
VERDE = "./assets/icons/verde.png"
BODY = "./assets/images/body.png"
LINEA_HORIZONTAL = "./assets/icons/linea_horizontal.png"
PUNTERO_ROJO = "./assets/icons/red_circle.png"
BOMBA = "./assets/icons/bomb.png"
MASCOTA_NORMAL = "./assets/images/normal.png"
FLECHA_DERECHA = "./assets/icons/drch.png"
FLECHA_IZQUIERDA = "./assets/icons/izq.png"
PDF = "./assets/icons/pdf.png"
MODIFY = "./assets/icons/modificar.png"

# Música
MUSIC_1 = "./assets/sound/music_1.wav"
MUSIC_2 = "./assets/sound/music_2.wav"
MUSIC_3 = "./assets/sound/music_3.wav"
MUSIC_4 = "./assets/sound/music_4.wav"
MUSIC_5 = "./assets/sound/music_5.wav"
MUSIC_6 = "./assets/sound/music_6.wav"
MUSIC = [MUSIC_1,MUSIC_2,MUSIC_3,MUSIC_4,MUSIC_5,MUSIC_6]

# Miniaturas
MINIATURA_DIAGONALES = "./assets/images/miniatura_diagonales.png"
MINIATURA_SQUAD = "./assets/images/miniatura_squad.png"
MINIATURA_BALLS = "./assets/images/miniatura_balls.png"
# Tutorial


# Animation folder
EXPLOSION = "./assets/animations/explosion"
FIREWORKS = "./assets/animations/fireworks"
SQUADGIF = "./assets/animations/squad"
BALLGIF = "./assets/animations/ball"

# Letter size
SMALL_FONT = 18
MEDIUM_FONT = 24
MEDIUM_ARIAL_FONT = 35
BIG_ARIAL_FONT = 45
BIG_FONT = 55
HEADER_FONT = 80
EXTRABIG_FONT = 140
# Fonts
FONT = "./assets/fonts/Delight.ttf"

pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(FONT, SMALL_FONT)
FONTS["medium"] = pygame.font.Font(FONT, MEDIUM_FONT)
FONTS["big"] = pygame.font.Font(FONT, BIG_FONT)
FONTS["header"] = pygame.font.Font(FONT, HEADER_FONT)
FONTS["extra"] = pygame.font.Font(FONT, EXTRABIG_FONT)
FONTS["arial_small"] = pygame.font.SysFont("arial", SMALL_FONT)
FONTS["arial_medium"] = pygame.font.SysFont("arial", MEDIUM_ARIAL_FONT)
FONTS["arial_big"] = pygame.font.SysFont("arial", BIG_ARIAL_FONT)

# Sounds
CLICKS = "./assets/sound/correct.wav"
EXPLOSION_SOUND = "./assets/sound/explosion.wav"
CLAPS = "./assets/sound/claps.wav"
PIP = "./assets/sound/pi.wav"

# Screen
WIDTH = 1280
HEIGHT = 780
MARGIN = 50

# Game settings
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRIS = "#1a232e"
AZUL_CLARO = "#3194cf"
AZUL_MARINO = "#317bcf"
COLOR_ROJO = "#ff0000"
GRISCLARO = "#9b9b9b"

# GAMA DE COLORES
GRANATE = "#7a3e48"
AMARILLO = "#eecd86"
NARANJA = "#e18942"
MARRON = "#b95835"
AZULGRISACEO = "#3d3242"

# FOR APP
TIME_BUTTONS = 2.5
WIDTH_LOAD_BAR = 700

# FOR GAME 1
ID_DIAGONALES = 1
VELOCIDAD_ENTRE_BOLAS = 2
PORCENTAJE_TRAMPAS = 0.2
FPS_EXPLOSION = 0.2
FPS_FIREWORKS = 0.2
TIEMPO_JUEGO = 60
VISIBILIDAD = 0.8
FEET_MARGIN = 30
FEET_BOX = 50
MANOS_IMG = ROCKET
ERROR = BOMBA
ACIERTO = ESTRELLA
MUSIC_DIAGONALES = "./assets/sound/music_1.wav"

# PUNTUACION
ACIERTO_PTO = 100
FALLO_PTO = 50

# MEDIAPIPE
BODY_PARTS = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28, 30, 31, 32]

# For squads
ID_SQUAD = 2
VELOCIDAD_SQUAD = 5
TIEMPO_JUEGO_SQUAD = 30
FPS_SQUAD = 20

# For balls
ID_BALLS = 3
VELOCIDAD_BALL = 7
TIEMPO_JUEGO_BALL = 40
FPS_BALL = 20

# BALL COLORS AVAILABLE
LOW_RED = [161, 155, 84]
HIGH_RED = [179, 255, 255]
LOW_BLUE = [94, 80, 2]
HIGH_BLUE = [126, 255, 255]
LOW_GREEN = [25, 52, 72]
HIGH_GREEM = [102, 255, 255]
LOW_YELLOW = [20, 100, 100]
HIGH_YELLOW = [40, 255, 255]

BALL_COLOR_LOWER = LOW_YELLOW
BALL_COLOR_UPPER = HIGH_YELLOW