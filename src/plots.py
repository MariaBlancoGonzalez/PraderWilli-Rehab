import matplotlib.backends.backend_agg as agg
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")


def create_right_hand_two_lines(errores, aciertos, fecha, mano):
    fig = plt.figure(figsize=[8, 2.8],  # Inches
                     dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                     facecolor=(0.9333, 0.8039, 0.5255, 1))
    # plt.title('Evolución mano izquierda', fontsize=16)
    ax = fig.add_subplot(111)
    ax.set_title(f'Evolución mano {mano}')
    fig.tight_layout()
    plt.margins(0)

    ax.plot(fecha, aciertos, c='b', label='Aciertos')
    ax.plot(fecha, errores, c='r', label='Errores')

    ax.set_ylim(0, max((aciertos+errores))+1)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
              ncol=3, fancybox=True, shadow=True)

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return canvas, raw_data


def create_pdf_graphics(errores, aciertos, fecha, mano):
    # Configurar el tamaño de la figura
    fig = plt.figure(figsize=(5.5, 2.5), dpi=100)

    ax = fig.add_subplot(111)
    ax.set_title(f'Mano {mano}')

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Resultados')

    ax.plot(fecha, errores, color='red', label='Errores')
    ax.plot(fecha, aciertos, color='blue', label='Aciertos')

    for i, v in enumerate(errores):
        ax.text(i, v + 0.5, str(v), ha='center', fontsize= 8)
    for i, v in enumerate(aciertos):
        ax.text(i, v + 0.5, str(v), ha='center', fontsize= 8)

    ax.legend()
    return fig
