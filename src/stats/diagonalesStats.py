from utils import *
import stats.plots as plt
from stats.calc import *
from broker import No_DB
from ui.table import Tabla
from settings.settings_0 import EXER_0_JSON
from settings.settings_0 import ID_DIAGONALES

class DiagonalesStats:
    def __init__(self, txt_exer, id_exer, ventana):
        self.name = txt_exer
        self.id_exer = id_exer
        self.data = []
        self.graphs = []
        self.stats = []
        self.table = None
        self.window = ventana

    def create_measures(self):
        json_object = No_DB()
        self.data = json_object.read_json(EXER_0_JSON, ID_DIAGONALES)
            
        if self.data != []:
            tiempo, tiempo_ejer, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos = distribute_data(self.data)  
            tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tiempo_ejer = sumar_valores_misma_fecha_diag(tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tiempo_ejer)
            
            self.create_stats(tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos)
            self.create_graphs(tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tiempo_ejer)

    def create_table(self, pos):
        header = ('Fecha','Tiempo','Error izquierda','Acierto izquierda', 'Error derecha', 'Acierto derecha')
        
        self.table = Tabla(self.id_exer, self.window, self.data, header, pos)

    def create_graphs(self, tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tiempo_ejer):
        canvas_izq, raw_data_izq = plt.create_groupbar_chart_squad(
            tiempo, izq_errores, izq_aciertos, tiempo_ejer, "izquierda", 'Alcanzadas')
        size_izq = canvas_izq.get_width_height()

        surf_izq = pygame.image.fromstring(raw_data_izq, size_izq, "RGB")
        self.graphs.append(('Izquierda', surf_izq))

        canvas_drcha, raw_data_drcha = plt.create_groupbar_chart_squad(tiempo, drcha_errores, drcha_aciertos, tiempo_ejer, "derecha", 'Alcanzadas')
        size_drcha = canvas_drcha.get_width_height()

        surf_drcha = pygame.image.fromstring(raw_data_drcha, size_drcha, "RGB")
        self.graphs.append(('Derecha', surf_drcha))

    def create_stats(self, tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos):
        best_score, best_day = 0, 0
        media_total_fallos, media_total_aciertos = 0, 0
        media_errores_d, media_errores_i = 0, 0

        best_score, best_day = get_best_score(self.data)
        self.stats.append(('-Mejor marca: ', best_score))
        self.stats.append(('-Fecha: ', best_day))

        media_total_aciertos = calculate_media_total(
            izq_aciertos, drcha_aciertos
        )
        self.stats.append(('-Media de aciertos: ', round(media_total_aciertos,2)))

        media_total_fallos = calculate_media_total(
            izq_errores, drcha_errores
        )
        self.stats.append(('-Media de errores : ', round(media_total_fallos,2)))
        
        media_aciertos_d = calculate_media_parte(drcha_aciertos)
        media_aciertos_i = calculate_media_parte(izq_aciertos)
        self.stats.append(('-Media de aciertos derecha: ', round(media_aciertos_d,2)))
        self.stats.append(('-Media de aciertos izquierda: ', round(media_aciertos_i,2)))

        media_errores_d = calculate_media_parte(drcha_errores)
        media_errores_i = calculate_media_parte(izq_errores)
        self.stats.append(('-Media de errores derecha: ', round(media_errores_d,2)))
        self.stats.append(('-Media de errores izquierda: ', round(media_errores_i,2)))
