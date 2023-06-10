import pygame

# Texts
CAPTION = "Prader Willi"

# Data
EXER_0_JSON = './data/0.json'
EXER_1_JSON = './data/1.json'
EXER_2_JSON = './data/2.json'

# Config
EXER_0_CONFIG = './config/Exer_0_config.json'
EXER_1_CONFIG = './config/Exer_1_config.json'
EXER_2_CONFIG = './config/Exer_2_config.json'

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
FLECHA_DERECHA = "./assets/icons/drch.png"
FLECHA_IZQUIERDA = "./assets/icons/izq.png"
PDF = "./assets/icons/pdf.png"
MODIFY = "./assets/icons/modificar.png"
FOOTBALL = "./assets/icons/pelota.png"
BASKETBALL = "./assets/icons/pelota-de-baloncesto.png"
TENISBALL = "./assets/icons/tenis.png"
RUGBYBALL = "./assets/icons/futbol-americano.png"

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
DIAGGIF = "./assets/animations/diagonales"

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
TIMES_FONT = "./assets/fonts/times_new_roman.ttf"

pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(FONT, SMALL_FONT)
FONTS["medium"] = pygame.font.Font(FONT, MEDIUM_FONT)
FONTS["big"] = pygame.font.Font(FONT, BIG_FONT)
FONTS["header"] = pygame.font.Font(FONT, HEADER_FONT)
FONTS["extra"] = pygame.font.Font(FONT, EXTRABIG_FONT)
FONTS["arial_small"] = pygame.font.Font(TIMES_FONT, SMALL_FONT)
FONTS["arial_medium"] = pygame.font.Font(TIMES_FONT, MEDIUM_ARIAL_FONT)
FONTS["arial_big"] = pygame.font.Font(TIMES_FONT, BIG_ARIAL_FONT)

# Sounds
CLICKS = "./assets/sound/correct.wav"
EXPLOSION_SOUND = "./assets/sound/explosion.wav"
CLAPS = "./assets/sound/claps.wav"
PIP = "./assets/sound/pi.wav"
ERROR_SOUND = "./assets/sound/error.wav"

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
AMARILLO_OSCURO = "#e8bb59"
RED = "#ff0000"
# GAMA DE COLORES
GRANATE = "#7a3e48"
AMARILLO = "#eecd86"
NARANJA = "#e18942"
MARRON = "#b95835"
AZULGRISACEO = "#3d3242"

# FOR APP
TIME_BUTTONS = 2.5
WIDTH_LOAD_BAR = 700

# FOR GAME DIAGONALES
ID_DIAGONALES = 0
FPS_EXPLOSION = 0.2
FPS_FIREWORKS = 0.2
VISIBILIDAD = 0.8
FEET_MARGIN = 30
FEET_BOX = 50
MANOS_IMG = ROCKET
ERROR = BOMBA
ACIERTO = ESTRELLA
FPS_DIAG = 20

# PUNTUACION
ACIERTO_PTO = 100
FALLO_PTO = 50

# MEDIAPIPE
BODY_PARTS = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28, 30, 31, 32]

# For squads
ID_SQUAD = 1
FPS_SQUAD = 20

# For balls
ID_BALLS = 2
ACIERTO_BALLS = 10
FALLO_BALLS = 10
FPS_BALLS = 20