# Module Imports
import mariadb as db
import logging
import sys
import configparser
import datetime
import json
logging.getLogger().setLevel(logging.INFO)

class DataBroker:
    def __init__(self):
        today = datetime.date.today()
        self.today = today.strftime("%Y-%m-%d")

    def write_data_json(self, file, id_game, time, element1=0, element2=0, element3=0, element4=0, element5 = 0, element6=0,element7=0,element8=0):
        if id_game == 0:
            new_data = {
                "PT_fecha": self.today, "PT_tiempo": time,
                "PT_fallos_izquierda": element1,
                "PT_aciertos_izquierda": element2,
                "PT_fallos_derecha": element3,
                "PT_aciertos_derecha": element4,
                "PT_tiempo_reaccion_errores_izquierda":element5,
                "PT_tiempo_reaccion_aciertos_izquierda":element6,
                "PT_tiempo_reaccion_errores_derecha":element7,
                "PT_tiempo_reaccion_errores_derecha":element8,
            }
        elif id_game == 1:
            new_data = {
                "PT_fecha": self.today, "PT_tiempo": time,
                "PT_errores": element1,
                "PT_aciertos": element2,
                "PT_media_angulo": element3,
            }
        elif id_game == 2:
            new_data = {
                "PT_fecha": self.today, "PT_tiempo": time,
                "PT_errores": element1,
                "PT_total_bolas": element2,
            }

        with open(file, 'r') as f:
            data = json.load(f)

        data.append(new_data)

        with open(file, 'w') as f:
            json.dump(data, f)

    def read_json(self, file, id_game):
        data_final = []
        with open(file, 'r') as f:
            data = json.load(f)

        if id_game == 0:
            for score in data:
                date = datetime.datetime.strptime(score['PT_fecha'], '%Y-%m-%d').date()
                values = [
                    date,
                    score['PT_tiempo'],
                    score['PT_fallos_izquierda'],
                    score['PT_aciertos_izquierda'],
                    score['PT_fallos_derecha'],
                    score['PT_aciertos_derecha'],
                    score["PT_tiempo_reaccion_errores_izquierda"],
                    score["PT_tiempo_reaccion_aciertos_izquierda"],
                    score["PT_tiempo_reaccion_errores_derecha"],
                    score["PT_tiempo_reaccion_errores_derecha"],
                ]
                data_final.append(tuple(values))
        elif id_game == 1:
            for score in data:
                date = datetime.datetime.strptime(score['PT_fecha'], '%Y-%m-%d').date()
                values = [
                    date,
                    score['PT_tiempo'],
                    score['PT_errores'],
                    score['PT_aciertos'],
                    score['PT_media_angulo']
                ]
                data_final.append(tuple(values))
        elif id_game == 2:
            for score in data:
                date = datetime.datetime.strptime(score['PT_fecha'], '%Y-%m-%d').date()
                values = [
                    date,
                    score['PT_tiempo'],
                    score['PT_errores'],
                    score['PT_total_bolas'],
                ]
                data_final.append(tuple(values))
        return data_final