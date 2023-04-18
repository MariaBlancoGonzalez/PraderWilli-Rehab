# For statistics
def calculate_media_total(data1, data2):
    return sum(data1 + data2) / len(data1 + data2)


def get_best_score(data):
    new_datos = [[i[3], i[6] + i[8]] for i in data]
    max, date = 0, None
    for i in new_datos:
        if i[1] >= max:
            max = i[1]
            date = i[0]
    return max, date.strftime("%d/%m")


def calculate_media_parte(data):
    return sum(data) / len(data)
