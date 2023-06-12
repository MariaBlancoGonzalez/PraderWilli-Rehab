import math
from utils import *
import stats.plots as plt
from stats.calc import *
from broker import No_DB
import statistics
import json
from ui.table import Tabla
from settings import EXER_1_JSON
from settings import ID_SQUAD

class SquadStats:
    def __init__(self, txt_exer, id_exer, id_user, ventana):
        self.name = txt_exer
        self.id_exer = id_exer
        self.id_user = id_user

        self.data = []
        self.graphs = []
        self.stats = []
        self.window = ventana

    def create_measures(self):
        json_object = No_DB()
        self.data = json_object.read_json(EXER_1_JSON, ID_SQUAD)

        if self.data != []:
            fecha, errores, aciertos, media_angulo, tiempo = distribute_data_squad(
                self.data)
    
            fecha, errores, aciertos,media_angulo, tiempo = sumar_valores_misma_fecha_squad(
                fecha, errores, aciertos,media_angulo, tiempo)

            self.create_stats(fecha, errores, aciertos, media_angulo, tiempo)
            self.create_graphs(fecha, errores, aciertos, media_angulo, tiempo)

    def create_table(self, pos):
        header = ('Fecha','Tiempo','Errores','Squad correctas', 'Ángulo medio')
        
        self.table = Tabla(self.id_exer, self.window, self.data, header, pos)
        
    def create_graphs(self, fecha, errores, aciertos, media_angulo, tiempo):
        canvas, raw_data = plt.create_groupbar_chart_squad(
            fecha, errores, aciertos, tiempo)
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.graphs.append(('Errores/Aciertos', surf))

        canvas, raw_data = plt.create_line_chart(media_angulo, fecha, tiempo)
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.graphs.append(('Ángulo', surf))

    def create_stats(self, fecha, errores, aciertos, media_angulo, tiempo):        
        acierto_tiempo, best_score_day, best_score_acierto, time_of_best_day = get_best_day(aciertos, fecha, tiempo)
        # Este método tambien sirve para el peor
        errores_tiempo, worst_score_day, worst_score_error, time_of_worst_day = get_best_day(
            errores, fecha, tiempo)
        
        self.stats.append(('-Mejor marca sentadilla/tiempo: ', best_score_acierto))
        self.stats.append(('-Sentadiila/segundos: ', acierto_tiempo))
        self.stats.append(('-Fecha de esta marca: ', best_score_day))
        self.stats.append(('-Tiempo empleado en esta marca: ', time_of_best_day))
        
        self.stats.append(('-Peor marca errores/tiempo: ', worst_score_error))
        self.stats.append(('-Errores/segundos: ', errores_tiempo))
        self.stats.append(('-Fecha de esta marca: ', worst_score_day))
        self.stats.append(('-Tiempo empleado en esta marca: ', time_of_worst_day))
        self.stats.append(('-Media de ángulo actual: ', round(statistics.mean(media_angulo), 2)))
