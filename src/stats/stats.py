from utils import *
import stats.plots as plt
from stats.calc import *
from broker import DataBroker
import statistics

from ui.table import Tabla

class Stats:
    def __init__(self, id_exer, ventana, json):
        self.id_exer = int(id_exer)
        self.json = json
        self.data = []
        self.graphs = []
        self.stats = []
        self.window = ventana
        self.table = None

    def create_measures(self, dim):
        json_object = DataBroker()
        if self.id_exer == 0:
            self.data = json_object.read_json(self.json, self.id_exer)

            if self.data != []:
                tiempo, tiempo_ejer, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tr_errores_izquierda, tr_aciertos_izquierda, tr_errores_derecha, tr_aciertos_derecha = distribute_data(self.data)  
                tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tiempo_ejer = sumar_valores_misma_fecha_diag(tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tiempo_ejer)
                
                self.create_stats_0(tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tr_errores_izquierda, tr_aciertos_izquierda, tr_errores_derecha, tr_aciertos_derecha)
                self.create_graphs_0(dim, tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tiempo_ejer)

        elif self.id_exer == 1:

            self.data = json_object.read_json(self.json, self.id_exer)

            if self.data != []:
                fecha, errores, aciertos, media_angulo, tiempo = distribute_data_squad(
                    self.data)
        
                fecha, errores, aciertos,media_angulo, tiempo = sumar_valores_misma_fecha_squad(
                    fecha, errores, aciertos,media_angulo, tiempo)

                self.create_stats_1(fecha, errores, aciertos, media_angulo, tiempo)
                self.create_graphs_1(dim, fecha, errores, aciertos, media_angulo, tiempo)

        elif self.id_exer == 2:
            self.data = json_object.read_json(self.json, self.id_exer)

            if self.data != []:
                fecha, errores, aciertos, tiempo = distribute_data_stats(
                    self.data)
                fecha, errores, aciertos, tiempo = sumar_valores_misma_fecha(
                    fecha, errores, aciertos, tiempo)

                self.create_stats_2(fecha, errores, aciertos, tiempo)
                self.create_graphs_2(dim, fecha, errores, aciertos, tiempo)

    def create_table(self, pos):
        if self.id_exer == 0:
            header = ('Fecha','Tiempo','Error I','Acierto I', 'Error D', 'Acierto D', 'TR Error I', 'TR Acierto I', 'TR Error D', 'TR Acierto D')
            self.table = Tabla(self.id_exer, self.window, self.data, header, pos,  (100,30))
        
        elif self.id_exer == 1:
            header = ('Fecha','Tiempo','Errores','Squad correctas', 'Ángulo medio')
            self.table = Tabla(self.id_exer, self.window, self.data, header, pos)
        else:
            header = ('Fecha','Tiempo','Bolas impactadas','Bolas totales')
        
            self.table = Tabla(self.id_exer, self.window, self.data, header, pos)
    
    def create_graphs_0(self,dim,  tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tiempo_ejer):
        canvas_izq, raw_data_izq = plt.create_groupbar_chart_squad(dim, tiempo, izq_errores, izq_aciertos, tiempo_ejer, "izquierda", 'Alcanzadas')
        size_izq = canvas_izq.get_width_height()

        surf_izq = pygame.image.fromstring(raw_data_izq, size_izq, "RGB")
        self.graphs.append(('Izquierda', surf_izq))

        canvas_drcha, raw_data_drcha = plt.create_groupbar_chart_squad(dim,tiempo, drcha_errores, drcha_aciertos, tiempo_ejer, "derecha", 'Alcanzadas')
        size_drcha = canvas_drcha.get_width_height()

        surf_drcha = pygame.image.fromstring(raw_data_drcha, size_drcha, "RGB")
        self.graphs.append(('Derecha', surf_drcha)) 
    
    def create_graphs_1(self, dim, fecha, errores, aciertos, media_angulo, tiempo):
        canvas, raw_data = plt.create_groupbar_chart_squad(dim, fecha, errores, aciertos, tiempo)
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.graphs.append(('Errores/Aciertos', surf))

        canvas, raw_data = plt.create_line_chart(dim, media_angulo, fecha, tiempo)
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.graphs.append(('Ángulo', surf))
    
    def create_graphs_2(self, dim, fecha, errores, aciertos, tiempo):
        canvas, raw_data = plt.create_groupbar_chart(dim, 
            fecha, errores, aciertos, tiempo)
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.graphs.append(('Izquierda', surf))

    def create_stats_0(self, tiempo, izq_errores, izq_aciertos, drcha_errores, drcha_aciertos, tr_errores_izquierda, tr_aciertos_izquierda, tr_errores_derecha, tr_aciertos_derecha):
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

        # Tiempo reacción
        self.stats.append(('-Tiempo reacción errores izquierda: ', round(statistics.mean(tr_errores_izquierda),2)))
        self.stats.append(('-Tiempo reacción aciertos izquierda: ', round(statistics.mean(tr_aciertos_izquierda),2)))
        self.stats.append(('-Tiempo reacción errores derecha: ', round(statistics.mean(tr_errores_derecha),2)))
        self.stats.append(('-Tiempo reacción aciertos derecha: ', round(statistics.mean(tr_aciertos_derecha),2)))

    def create_stats_1(self, fecha, errores, aciertos, media_angulo, tiempo):       
        acierto_tiempo, best_score_day, best_score_acierto, time_of_best_day = get_best_day(aciertos, fecha, tiempo)
        # Este método tambien sirve para el peor
        errores_tiempo, worst_score_day, worst_score_error, time_of_worst_day = get_best_day(
            errores, fecha, tiempo)
        
        self.stats.append(('-Mejor marca sentadilla/tiempo: ', best_score_acierto))
        self.stats.append(('-Sentadilla/segundos: ', acierto_tiempo))
        self.stats.append(('-Fecha de esta marca: ', best_score_day))
        self.stats.append(('-Tiempo empleado en esta marca: ', time_of_best_day))
        
        self.stats.append(('-Peor marca errores/tiempo: ', worst_score_error))
        self.stats.append(('-Errores/segundos: ', errores_tiempo))
        self.stats.append(('-Fecha de esta marca: ', worst_score_day))
        self.stats.append(('-Tiempo empleado en esta marca: ', time_of_worst_day))
        self.stats.append(('-Media de ángulo actual: ', round(statistics.mean(media_angulo), 2)))

    def create_stats_2(self, fecha, errores, bolas_totales, tiempo):
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

