import math
from utils import *
import stats.plots as plt
from stats.calc import *
from broker import Broker
import statistics
import json
from ui.table import Tabla
import datetime
from settings import EXER_2_JSON

class BallStats:
    def __init__(self, txt_exer, id_exer, id_user, connection, ventana):
        self.name = txt_exer
        self.id_exer = id_exer
        self.id_user = id_user

        self.connect = connection

        self.data = []
        self.graphs = []
        self.stats = []
        self.window = ventana

    def create_table(self, pos):
        header = ('Fecha','Tiempo','Error izquierda','Acierto izquierda', 'Error derecha', 'Acierto derecha')
        
        self.table = Tabla(self.id_exer, self.window, self.data, header, pos)

    def create_measures(self):
        self.get_data()
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
        self.stats.append(('-Mejor marca esquivadas/tiempo: ', round(esquiva_tiempo, 2)))
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

    def get_data(self):
        if self.connect == 0:
            self.get_data_online()
        else:
            self.get_data_json()

    def get_data_online(self):
        broker = Broker()
        broker.connect()
        self.data = broker.get_score(self.id_exer, self.id_user, 10)
        broker.delete_temporary_table()
        broker.close()

    def get_data_json(self):
        with open(EXER_2_JSON, 'r') as f:
            data = json.load(f)
        for score in data:
            date = datetime.datetime.strptime(score['PT_fecha'], '%Y-%m-%d').date()
            values = [
                0,
                score['PT_A_id'],
                score['PT_E_id'],
                date,
                score['PT_tiempo'],
                score['PT_fallos_izquierda'],
                score['PT_aciertos_izquierda'],
                score['PT_fallos_derecha'],
                score['PT_aciertos_derecha']
            ]
            self.data.append(tuple(values))