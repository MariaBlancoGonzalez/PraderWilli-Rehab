from utils import *
import stats.plots as plt
from stats.calc import *
from broker import No_DB
import statistics

from ui.table import Tabla
import datetime
from settings import EXER_2_JSON
from settings import ID_BALLS

class BallStats:
    def __init__(self, txt_exer, id_exer, id_user, ventana):
        self.name = txt_exer
        self.id_exer = id_exer
        self.id_user = id_user

        self.data = []
        self.graphs = []
        self.stats = []
        self.window = ventana

    def create_table(self, pos):
        header = ('Fecha','Tiempo','Bolas impactadas','Bolas totales')
        
        self.table = Tabla(self.id_exer, self.window, self.data, header, pos)

    def create_measures(self):
        json_object = No_DB()
        self.data = json_object.read_json(EXER_2_JSON, ID_BALLS)

        if self.data != []:
            fecha, errores, aciertos, tiempo = distribute_data_stats(
                self.data)
            fecha, errores, aciertos, tiempo = sumar_valores_misma_fecha(
                fecha, errores, aciertos, tiempo)

            self.create_stats(fecha, errores, aciertos, tiempo)
            self.create_graphs(fecha, errores, aciertos, tiempo)

    def create_graphs(self, fecha, errores, aciertos, tiempo):
        canvas, raw_data = plt.create_groupbar_chart(
            fecha, errores, aciertos, tiempo)
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.graphs.append(('Izquierda', surf))

    def create_stats(self, fecha, errores, bolas_totales, tiempo):
        media_impactos = statistics.mean(errores)
        esquivadas = restar_arrays(bolas_totales, errores)
        esquiva_tiempo, best_score_day, best_score_acierto, time_of_best_day = get_best_day(
            esquivadas, fecha, tiempo)
        # Este método tambien sirve para el peor
        errores_tiempo, worst_score_day, worst_score_error, time_of_worst_day = get_best_day(
            errores, fecha, tiempo)
        self.stats.append(('-Media de bolas impactadas total: ',
                           round(media_impactos, 2)))
        
        self.stats.append(('-Promedio esquivadas/tiempo: ', round(esquiva_tiempo, 2)))
        self.stats.append(
            ('-Mejor marca esquivadas/tiempo: ', best_score_acierto))
        self.stats.append(('-Fecha de esta marca: ', best_score_day))
        self.stats.append(
            ('-Tiempo empleado en esta marca: ', time_of_best_day))
        
        self.stats.append(('-Peor marca impacto/tiempo: ', worst_score_error))
        self.stats.append(('-Impacto/segundos: ', errores_tiempo))
        self.stats.append(('-Fecha de esta marca: ', worst_score_day))
        self.stats.append(
            ('-Tiempo empleado en esta marca: ', time_of_worst_day))

        self.stats.append(('-Errores totales: ', sum(errores)))
        self.stats.append(('-Bolas totales: ', sum(bolas_totales)))
