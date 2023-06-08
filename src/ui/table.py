import pygame
import settings
import math
class Tabla:
    def __init__(self, id, ventana, datos_tabla, header, pos = 0, dimensiones_celda=(150, 30), color_borde=settings.BLACK, color_fondo=settings.WHITE, color_texto=settings.BLACK):    
        self.id = id
        self.ventana = ventana
        self.header = header
        self.name_actividad = None
        self.datos_tabla = self.set_data(datos_tabla)        
        self.current_datos = self.datos_tabla[:10]

        self.page = 1
        self.pages_available = math.ceil((len(datos_tabla))/10)

        self.dimensiones_celda = dimensiones_celda
        self.color_borde = color_borde
        self.color_fondo = color_fondo
        self.color_texto = color_texto

        self.ancho_celda, self.alto_celda = dimensiones_celda
        self.alto_tabla = len(datos_tabla) * self.alto_celda
        self.alto_ventana = ventana.get_height()
        
        try:
            self.x = (ventana.get_width() - self.ancho_celda * len(self.datos_tabla[0])) // 2
            self.y = 250
        except IndexError:
            pass

    def set_data(self, datos):
        if int(self.id) == 0:
            datos = self.remove_first_three_elements(datos)
            self.name_actividad = 'Diagonales Superiores'
        elif int(self.id) == 1:
            datos = self.remove_first_three_elements(datos)
            datos = self.remove_last_element(datos)
            self.name = 'Squads'
        elif int(self.id) == 2:
            datos = self.remove_first_three_elements(datos)
            self.name = 'Movilidad'
        return datos

    def remove_last_element(self, datos):
        result = []
        for tup in datos:
            new_tup = tup[:-1]
            result.append(new_tup)
        return result

    def remove_first_three_elements(self, datos):
        result = []
        for tup in datos:
            new_tup = tup[3:]
            result.append(new_tup)
        return result

    def update_page(self, pos):
        if pos == 1:
            if self.pages_available <  self.page+1:
                datos = self.current_datos
            elif self.pages_available >=  self.page+1:
                datos = self.current_datos
                datos = datos[1:]
                num = self.page * 10
                datos = self.datos_tabla[num:num+10]
                self.page += 1
            self.current_datos = datos

        if pos == -1:
            
            if self.page-1 < 1:
                datos = self.current_datos
            elif self.page-1 >= 1:
                datos = self.current_datos
                datos = datos[1:]
                num = self.page * 10 # donde estoy ahora mismo
                datos = self.datos_tabla[(self.page-1)*10-10:num] if num-10 >= 0 else self.datos_tabla[0:10]
                self.page -= 1
            self.current_datos = datos

    def dibujar(self, pos):
        rect_stats = pygame.Surface((1000, 425))  # the size of your rect
        rect_stats.set_alpha(128)  # alpha level
        # this fills the entire surface
        rect_stats.fill((255, 255, 255))
        self.ventana.blit(rect_stats, (140, 200))

        nombre = settings.FONTS["medium"].render(f"Datos recogidos en la actividad: {self.name_actividad}", True, settings.BLACK)
        self.ventana.blit(nombre, (145, 210))

        counter_celdas = 0
        if not all(isinstance(tupla, str) for tupla in self.current_datos[0]):
            self.current_datos.insert(0, self.header)

        for fila, datos_fila in enumerate(self.current_datos):
            if counter_celdas <= 10:
                for columna, contenido in enumerate(datos_fila):
                    # Calcular las coordenadas de la celda
                    x_celda = self.x + columna * self.ancho_celda 
                    y_celda = self.y + fila * self.alto_celda  

                    # Verificar si la celda está visible en la ventana
                    if y_celda + self.alto_celda < 0 or y_celda > self.alto_ventana:
                        continue

                        # Dibujar el fondo de la celda
                    pygame.draw.rect(self.ventana, self.color_fondo, (x_celda, y_celda, self.ancho_celda, self.alto_celda))

                        # Dibujar el borde de la celda
                    pygame.draw.rect(self.ventana, self.color_borde, (x_celda, y_celda, self.ancho_celda, self.alto_celda), 1)

                        # Dibujar el contenido de la celda
                    texto = settings.FONTS["arial_small"].render(str(contenido), True, settings.BLACK)
                    self.ventana.blit(texto, (x_celda + 5, y_celda + 5))
            counter_celdas+=1
        
        page = settings.FONTS["medium"].render(f"{str(self.page)}/{str(self.pages_available)}", True, settings.BLACK)
        self.ventana.blit(page, ((self.ventana.get_width()/2)-20, 650))