# For statistics
def calculate_media_total(data1, data2):
    return sum(data1 + data2) / len(data1 + data2)


def get_best_score(data):
    new_datos = [[i[0], i[3] + i[5]] for i in data]
    max, date = 0, None
    for i in new_datos:
        if i[1] >= max:
            max = i[1]
            date = i[0]
    return max, date.strftime("%d/%m")


def calculate_media_parte(data):
    return sum(data) / len(data)

def get_best_day(aciertos, fecha, tiempo):
    concatList = [(aciertos[i], tiempo[i]) for i in range(len(tiempo))]
    aciertos_segundo = [round((acierto/time), 3) for acierto, time in concatList]

    acierto_tiempo = max(aciertos_segundo)
    best_score_day = fecha[aciertos_segundo.index(max(aciertos_segundo))]
    best_score_acierto = aciertos[aciertos_segundo.index(max(aciertos_segundo))]
    time_of_best_day = tiempo[aciertos_segundo.index(max(aciertos_segundo))]

    return acierto_tiempo, best_score_day, best_score_acierto, time_of_best_day


def restar_arrays(a, b):
    resultado = []
    for i in range(len(a)):
        resultado.append(a[i] - b[i])
    return resultado
    
def sumar_valores_misma_fecha(fechas, errores, aciertos, tiempo):
    fechas_sumadas = []
    errores_sumados = []
    aciertos_sumados = []
    tiempo_sumado = []

    valores_sumados = {}

    for i in range(len(fechas)):
        fecha = fechas[i]
        valor_tiempo = tiempo[i]

        clave = (fecha, valor_tiempo)

        if clave in valores_sumados:
            valores_sumados[clave][0] += errores[i]
            valores_sumados[clave][1] += aciertos[i]
        else:
            valores_sumados[clave] = [errores[i], aciertos[i]]

    for clave, valores in valores_sumados.items():
        fecha, valor_tiempo = clave

        fechas_sumadas.append(fecha)
        errores_sumados.append(valores[0])
        aciertos_sumados.append(valores[1])
        tiempo_sumado.append(valor_tiempo)

    return fechas_sumadas, errores_sumados, aciertos_sumados, tiempo_sumado

def sumar_valores_misma_fecha_squad(fechas, errores, aciertos,media, tiempo):
    fechas_sumadas = []
    errores_sumados = []
    aciertos_sumados = []
    media_media = []
    tiempo_sumado = []

    valores_sumados = {}

    for i in range(len(fechas)):
        fecha = fechas[i]
        valor_tiempo = tiempo[i]

        clave = (fecha, valor_tiempo)

        if clave in valores_sumados:
            valores_sumados[clave][0] += errores[i]
            valores_sumados[clave][1] += aciertos[i]
            valores_sumados[clave][2] = valores_sumados[clave][2] if media[i]>valores_sumados[clave][2] else media[i]
        else:
            valores_sumados[clave] = [errores[i], aciertos[i], media[i]]

    for clave, valores in valores_sumados.items():
        fecha, valor_tiempo = clave

        fechas_sumadas.append(fecha)
        errores_sumados.append(valores[0])
        aciertos_sumados.append(valores[1])
        media_media.append(valores[2])
        tiempo_sumado.append(valor_tiempo)

    return fechas_sumadas, errores_sumados, aciertos_sumados, media_media, tiempo_sumado


def sumar_valores_misma_fecha_diag(fechas, errores, aciertos, errores_d, aciertos_d, tiempo):
    fechas_sumadas = []
    errores_sumados = []
    aciertos_sumados = []
    errores_sumados_d = []
    aciertos_sumados_d = []
    tiempo_sumado = []

    valores_sumados = {}

    for i in range(len(fechas)):
        fecha = fechas[i]
        valor_tiempo = tiempo[i]

        clave = (fecha, valor_tiempo)

        if clave in valores_sumados:
            valores_sumados[clave][0] += errores[i]
            valores_sumados[clave][1] += aciertos[i]
            valores_sumados[clave][2] += errores_d[i]
            valores_sumados[clave][3] += aciertos_d[i]
        else:
            valores_sumados[clave] = [errores[i], aciertos[i], errores_d[i], aciertos_d[i]]

    for clave, valores in valores_sumados.items():
        fecha, valor_tiempo = clave

        fechas_sumadas.append(fecha)
        errores_sumados.append(valores[0])
        aciertos_sumados.append(valores[1])
        errores_sumados_d.append(valores[2])
        aciertos_sumados_d.append(valores[3])
        tiempo_sumado.append(valor_tiempo)

    return fechas_sumadas, errores_sumados, aciertos_sumados, errores_sumados_d, aciertos_sumados_d, tiempo_sumado
