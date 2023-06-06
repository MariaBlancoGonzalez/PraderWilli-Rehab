from datetime import datetime, timedelta
import matplotlib.backends.backend_agg as agg
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("Agg")

def create_right_hand_two_lines(errores, aciertos, fecha, tiempo, mano):

    plt.style.use('ggplot')
    fig = plt.figure(
        figsize=[8, 2.8],  # Inches
        dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
        facecolor=(0.9333, 0.8039, 0.5255, 1),
    )
    ax = fig.add_subplot(111)
    ax.set_title(f"Evolución mano {mano}")
    fig.tight_layout()
    plt.margins(x=0.1, y=0.1)

    ax.plot(fecha, aciertos, c="b", label="Aciertos")
    ax.plot(fecha, errores, c="r", label="Errores")
    #ax.plot(fecha, tiempo, c="black", label="Tiempo")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=3,
        fancybox=True,
        shadow=True,
    )

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return canvas, raw_data

def create_line_chart(angulo, fecha, tiempo):

    plt.style.use('ggplot')
    fig = plt.figure(
        figsize=[8, 2.8],  # Inches
        dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
        facecolor=(0.9333, 0.8039, 0.5255, 1),
    )
    ax = fig.add_subplot(111)
    ax.set_title(f"Media de ángulo alcanzado por día")
    fig.tight_layout()
    plt.margins(x=0.1, y=0.1)

    ax.plot(fecha, angulo, c="b", label="Ángulo")
    #ax.plot(fecha, tiempo, c="black", label="Tiempo")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=3,
        fancybox=True,
        shadow=True,
    )

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return canvas, raw_data

def create_pdf_graphics(errores, aciertos, fecha, mano):
    # Configurar el tamaño de la figura
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(5.5, 2.5), dpi=100)

    ax = fig.add_subplot(111)
    ax.set_title(f"Mano {mano}")

    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Resultados")

    ax.plot(fecha, errores, color="red", label="Errores")
    ax.plot(fecha, aciertos, color="blue", label="Aciertos")

    for i, v in enumerate(errores):
        ax.text(i, v + 0.5, str(v), ha="center", fontsize=8)
    for i, v in enumerate(aciertos):
        ax.text(i, v + 0.5, str(v), ha="center", fontsize=8)

    ax.legend()
    return fig

def create_groupbar_chart_squad(fechas, errores, aciertos, tiempo):
    grouped = {
        'Errores': errores,
        'Correcto': aciertos,
        }

    plt.style.use('ggplot')
    x = np.arange(len(fechas))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0

    fig = plt.figure(
        figsize=[8, 2.8],  # Inches
        dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
        facecolor=(0.9333, 0.8039, 0.5255, 1),
    )
    # plt.title('Evolución mano izquierda', fontsize=16)
    ax = fig.add_subplot(111)

    for attribute, measurement in grouped.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Ejecuciones del ejercicio')
    ax.set_title('Resultados diarios')
    ax.set_xticks(x + width, fechas)
    ax.legend(loc='upper left', ncol=3)
    ax.set_ylim(0, max((errores+aciertos))+5)
    ax2 = ax.twinx()

    # Establecer los límites del segundo eje y
    #ax2.set_ylim(ax.get_ylim())
    ax2.plot(x + width, tiempo, color='red',
             marker='X', linestyle='dashed', label='Tiempo')
    ax2.set_ylabel('Tiempo (segundos)')
    ax2.legend(loc='upper right')

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return canvas, raw_data

def create_groupbar_chart(fechas, errores, aciertos, tiempo):
    esquivadas = [aciertos[i]-errores[i] for i in range(len(aciertos))]
    grouped = {
        'Impactos': errores,
        'Esquivadas': esquivadas,
        'Bolas Totales': aciertos}

    plt.style.use('ggplot')
    x = np.arange(len(fechas))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0

    fig = plt.figure(
        figsize=[8, 4],  # Inches
        dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
        facecolor=(0.9333, 0.8039, 0.5255, 1),
    )
    # plt.title('Evolución mano izquierda', fontsize=16)
    ax = fig.add_subplot(111)

    for attribute, measurement in grouped.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Ejecuciones del ejercicio')
    ax.set_title('Resultados diarios')
    ax.set_xticks(x + width, fechas)
    ax.legend(loc='upper left', ncol=3)
    ax.set_ylim(0, max((errores+aciertos))+5)

    ax2 = ax.twinx()

    # Establecer los límites del segundo eje y
    ax2.set_ylim(ax.get_ylim())
    ax2.plot(x + width, tiempo, color='red',
             marker='X', linestyle='dotted', label='Tiempo')
    ax2.set_ylabel('Tiempo (segundos)')
    ax2.legend(loc='upper right')
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return canvas, raw_data
    
def create_error_success_time_plot(fechas, errores, aciertos, tiempo):
    # Configurar estilo "ggplot"
    plt.style.use('ggplot')
    
    fig = plt.figure(
        figsize=[8, 4],  # Inches
        dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
        facecolor=(0.9333, 0.8039, 0.5255, 1),
    )
    ax = fig.add_subplot(111)

    ax.plot(fechas, aciertos, label='Aciertos', color='steelblue')
    ax.plot(fechas, errores, label='Errores', color='firebrick')
    ax.scatter(fechas, aciertos, color='steelblue')
    ax.scatter(fechas, errores, color='firebrick', marker='x')
    ax.set_title('Aciertos y Errores en Sentadillas')

    ax.set_xlabel('Fecha')
    ax.set_ylabel('Cantidad')
    ax.set_xticks(fechas)
    ax.xaxis.set_tick_params(rotation=45)
    ax.legend()
    fig.tight_layout()

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return canvas, raw_data
