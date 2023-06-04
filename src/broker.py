# Module Imports
import mariadb as db
import logging
import sys
import configparser
import datetime
import json
logging.getLogger().setLevel(logging.INFO)


class Broker:
    def __init__(self):
        self.cursor = ""

        self.cursor = None
        self.conn = None

    # Connect to MariaDB Platform
    def connect(self):
        # connection to the database
        config = configparser.ConfigParser()
        config.read(r"./docs/credenciales.ini")

        username = config.get("DB", "username")
        pwd = config.get("DB", "password")
        datab = config.get("DB", "db")
        db_host = config.get("DB", "host")
        db_port = config.getint("DB", "port")
        try:
            self.conn = db.connect(
                user=username, password=pwd, host=db_host, port=db_port, database=datab
            )
            self.cursor = self.conn.cursor()
            # Status success
            return 0
        except db.Error as e:
            # Status error
            return 1
        # Get Cursor

    def add_user(self, name, lastname):
        try:
            statement = f"INSERT INTO Alumno (A_nombre, A_apellido) VALUES ('{name}', '{lastname}')"
            self.cursor.execute(statement)
            self.conn.commit()
            logging.info("Successfully added entry to database")
        except db.Error as e:
            logging.error(f"Error adding entry to database: {e}")

    def get_user_id(self, name):
        statement = f"SELECT A_id FROM Alumno WHERE A_nombre={name}"
        try:
            self.cursor.execute(statement)
            return self.cursor.fetchall()[0][0]
        except db.Error as e:
            logging.error(f"Error retrieving entry from database: {e}")

    def get_user(self, id):
        statement = f"SELECT A_nombre FROM Alumno WHERE A_id={id}"
        try:
            self.cursor.execute(statement)
            return self.cursor.fetchall()[0][0]
        except db.Error as e:
            logging.error(f"Error retrieving entry from database: {e}")

    def get_users(self):
        try:
            statement = f"SELECT * FROM Alumno"
            self.cursor.execute(statement)
            users = []
            for i in self.cursor.fetchall():
                users.append((i[0], i[1], i[2]))
            return users
        except db.Error as e:
            logging.error(f"Error retrieving entry from database: {e}")

    def add_exercise(self, name):
        try:
            statement = f"INSERT INTO Ejercicio (E_nombre) VALUES ('{name}')"
            self.cursor.execute(statement)
            self.conn.commit()
            logging.info("Successfully added exercise to database")
        except db.Error as e:
            logging.error(f"Error adding entry to database: {e}")

    def get_exercise(self, id):
        try:
            statement = f"SELECT E_nombre FROM Ejercicio WHERE E_id={id}"
            self.cursor.execute(statement)
            return self.cursor.fetchall()[0][0]
        except db.Error as e:
            logging.error(f"Error retrieving entry from database: {e}")

    def add_score(
        self,
        alumno,
        ejercicio,
        fecha,
        tiempo,
        fallosizq,
        aciertosizq,
        fallosdrch,
        aciertosdrch,
    ):
        try:
            statement = f"INSERT INTO Puntuaciones (PT_A_id, PT_E_id, PT_fecha, PT_tiempo, PT_fallos_izquierda, PT_aciertos_izquierda, PT_fallos_derecha, PT_aciertos_derecha) VALUES ({alumno}, {ejercicio}, '{fecha}', {tiempo}, {fallosizq}, {aciertosizq}, {fallosdrch}, {aciertosdrch})"
            self.cursor.execute(statement)
            self.conn.commit()
            logging.info("Successfully added exercise to database")
        except db.Error as e:
            logging.error(f"Error adding entry to database: {e}")

    def get_last_score(self, PT_E_id, PT_A_id, number_score=20):
        query = f"SELECT * FROM Puntuaciones p WHERE p.PT_A_id = {int(PT_A_id)} and p.PT_E_id = {int(PT_E_id)} ORDER BY p.PT_id DESC LIMIT {number_score}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except db.Error as e:
            logging.error(f"Error getting information from the database: {e}")

    def get_score(self, PT_E_id, PT_A_id, number_score_days=10):
        query = f"SELECT * FROM Puntuaciones p WHERE p.PT_A_id = {int(PT_A_id)} and p.PT_E_id = {int(PT_E_id)} and p.PT_fecha >= DATE(NOW() - INTERVAL {number_score_days} DAY)"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except db.Error as e:
            logging.error(f"Error getting information from the database: {e}")

    def get_exercises(self):
        try:
            statement = f"SELECT * FROM Ejercicio"
            self.cursor.execute(statement)
            exer = []
            for i in self.cursor.fetchall():
                exer.append((i[0], i[1]))
            return exer
        except db.Error as e:
            logging.error(f"Error retrieving entry from database: {e}")

    def delete_user(self, name, surname):
        statement = (
            f"DELETE FROM Alumno WHERE A_nombre='{name}' and A_apellido='{surname}'"
        )
        try:
            self.cursor.execute(statement)
        except db.Error as e:
            logging.error(f"Error getting information from the database: {e}")

    # End
    def close(self):
        self.conn.close()

class No_DB:
    def __init__(self):
        self.a_id = 1
        today = datetime.date.today()
        self.today = today.strftime("%Y-%m-%d")

    def write_new_json(self):
        new_data = {
            "PT_E_id": self.id_game, "PT_fecha": self.today, "PT_tiempo": self.game_time,
            "PT_fallos_izquierda": errores_izquierda,
            "PT_aciertos_izquierda": aciertos_izquierda,
            "PT_fallos_derecha": errores_derecha,
            "PT_aciertos_derecha": aciertos_derecha
        }

    def create_json_file(self, file_name):
        dictionary = {"id": self.id_user,
                "puntuaciones":[]
        }

        jsonString = json.dumps(dictionary, indent=4)

        with open(file_name, "w") as outfile:
            outfile.write(jsonString)

    def write_data_json(self, file, id_game, time, errores_izquierda=0, aciertos_izquierda=0, errores_derecha=0, aciertos_derecha=0):
        new_data = {
            "PT_A_id": self.a_id, "PT_E_id": id_game, "PT_fecha": self.today, "PT_tiempo": time,
            "PT_fallos_izquierda": errores_izquierda,
            "PT_aciertos_izquierda": aciertos_izquierda,
            "PT_fallos_derecha": errores_derecha,
            "PT_aciertos_derecha": aciertos_derecha
        }

        with open(file, 'r') as f:
            data = json.load(f)

        data.append(new_data)

        with open(file, 'w') as f:
            json.dump(data, f)
