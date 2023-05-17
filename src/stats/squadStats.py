import math
from utils import *
import stats.plots as plt
from stats.calc import *
from broker import Broker

class SquadStats:
    def __init__(self, txt_exer, id_exer, id_user, connection):
        self.name = txt_exer
        self.id_exer = id_exer
        self.id_user = id_user

        self.connect = connection

        self.data = []
        self.graphs = []
        self.stats = []

    def create_measures(self):
        self.get_data()
        if self.data != []:
            fecha, errores, aciertos, caidas, tiempo = distribute_data_stats(
                self.data)

            self.create_stats(fecha, errores, aciertos, caidas, tiempo)
            self.create_graphs(fecha, errores, aciertos, caidas, tiempo)
        
    def create_graphs(self, fecha, errores, aciertos, caidas, tiempo):
        canvas, raw_data = plt.create_groupbar_chart(
            fecha, errores, aciertos, caidas, tiempo)
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.graphs.append(('Izquierda', surf))

    def create_stats(self, fecha, errores, aciertos, caidas, tiempo):
        cumulo_errores = [errores[i]+caidas[i] for i in range(len(aciertos))]
        
        acierto_tiempo, best_score_day, best_score_acierto, time_of_best_day = get_best_day(aciertos, fecha, tiempo)
        # Este método tambien sirve para el peor
        errores_tiempo, worst_score_day, worst_score_error, time_of_worst_day = get_best_day(
            cumulo_errores, fecha, tiempo)
        
        self.stats.append(('-Mejor marca correcto/tiempo: ', best_score_acierto))
        self.stats.append(('-Aciertos/segundos: ', acierto_tiempo))
        self.stats.append(('-Fecha de esta marca: ', best_score_day))
        self.stats.append(('-Tiempo empleado en esta marca: ', time_of_best_day))
        
        self.stats.append(('-Peor marca correcto/tiempo: ', worst_score_error))
        self.stats.append(('-Errores/segundos: ', errores_tiempo))
        self.stats.append(('-Fecha de esta marca: ', worst_score_day))
        self.stats.append(('-Tiempo empleado en esta marca: ', time_of_worst_day))

        self.stats.append(('-Errores+Caidas totales: ', sum(cumulo_errores)))
        self.stats.append(('-Aciertos totales: ', sum(aciertos)))

    def get_data(self):
        if self.connect == 0:
            self.get_data_online()
        else:
            self.get_data_json()

    def get_data_online(self):
        broker = Broker()
        broker.connect()
        self.data = broker.get_score(self.id_exer, self.id_user, 10)
        broker.close()

    def get_data_json(self):
        with open('default.json', 'r') as f:
            data = json.load(f)

        for score in data['puntuaciones']:
            date = datetime.datetime.strptime(score['PT_fecha'], '%Y-%m-%d')
            values = [
                score['PT_id'],
                score['PT_A_id'],
                score['PT_E_id'],
                date,
                score['PT_fecha'],
                score['PT_fallos_izquierda'],
                score['PT_aciertos_izquierda'],
                score['PT_fallos_derecha'],
                score['PT_aciertos_derecha']
            ]
            self.data.append(tuple(values))
