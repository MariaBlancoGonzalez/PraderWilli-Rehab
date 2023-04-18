from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph, Spacer
from reportlab.platypus.frames import Frame

from io import BytesIO
from svglib.svglib import svg2rlg

from datetime import datetime
from broker import Broker
from utils import distribute_data
from stats.calc import calculate_media_parte, calculate_media_total, get_best_score
from stats.plots import create_pdf_graphics

styles = getSampleStyleSheet()


class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, id_user, id_exercise):
        super().__init__(filename, pagesize=letter)
        self.addPageTemplates(self.createPageTemplate())
        self.space = Spacer(1, 20)
        self.id_user = id_user
        self.id_exercise = id_exercise
        self.user = ""
        self.exercise = ""
        self.data = []
        self.get_data()

    def get_data(self):
        broker = Broker()
        broker.connect()
        self.data = broker.get_last_score(self.id_user, self.id_exercise)
        self.user = broker.get_user(self.id_user)
        self.exercise = broker.get_exercise(self.id_exercise)
        broker.close()

    def createPageTemplate(self):
        frame = Frame(
            self.leftMargin, self.bottomMargin, self.width, self.height, id="normal"
        )
        template = PageTemplate(id="mainTemplate", frames=frame, onPage=self.addHeader)
        return template

    def addHeader(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawCentredString(
            doc.pagesize[0] / 2.0,
            doc.pagesize[1] - 40,
            f'Datos sobre {self.user} sobre la actividad {self.exercise}. Día {datetime.now().strftime("%d/%m/%Y")}',
        )
        canvas.restoreState()

    def parse_data(self, data):
        data_parsed = [
            [
                "Fecha",
                "Tiempo",
                "Fallos izquierda",
                "Aciertos izquierda",
                "Fallos derecha",
                "Aciertos derecha",
            ]
        ]
        for tup in data:
            new_list = list(tup)
            new_list.pop(0)
            new_list.pop(0)
            new_list.pop(0)
            new_list[0].strftime("%d/%m/%Y")
            new_list = tuple(new_list)
            data_parsed.append(new_list)

        return data_parsed

    def get_statistics(self):
        time, left_error, left_correct, right_error, right_correct = distribute_data(
            self.data
        )
        best_score, best_day = get_best_score(self.data)
        total_media_correct = calculate_media_total(left_correct, right_correct)
        total_media_error = calculate_media_total(left_error, right_error)
        media_error_left, media_error_right = calculate_media_parte(
            left_error
        ), calculate_media_parte(right_error)
        media_correct_left, media_correct_right = calculate_media_parte(
            left_correct
        ), calculate_media_parte(right_correct)
        line = "---------------------------------------------------------------------------------------------------------------------------------------"
        stats_str = (
            f"{line}<br/>Mejor marca: <b>{best_score}</b><br/> {line}<br/>Mejor día de realización: <b>{best_day}</b><br/>{line}<br/>"
            + f"Media total de aciertos con las dos manos: <b>{round(total_media_correct, 2)}</b><br/>{line}<br/>"
            + f"Media total de errores con las dos manos: <b>{round(total_media_error, 2)}</b><br/>{line}<br/>"
            + f"Media total de errores con la mano izquierda: <b>{round(media_error_left, 2)}</b><br/>{line}<br/>"
            + f"Media total de errores con la mano derecha: <b>{round(media_error_right, 2)}</b><br/>{line}<br/>"
            + f"Media total de aciertos con la mano izquierda: <b>{round(media_correct_left, 2)}</b><br/>{line}<br/>"
            + f"Media total de aciertos con la mano derecha: <b>{round(media_correct_right, 2)}</b><br/>{line}<br/>"
        )

        plot_left = create_pdf_graphics(left_error, left_correct, time, "izquierda")
        plot_right = create_pdf_graphics(right_error, right_correct, time, "derecha")

        """# Crear una imagen a partir del canvas de Matplotlib
        canvas_image_right = plot_right.get_renderer()
        canvas_image_left = plot_left.get_renderer()"""

        return stats_str, plot_left, plot_right

    def create_table(self, data):
        data = self.parse_data(data)
        c_width = [
            0.9 * inch,
            0.7 * inch,
            1.2 * inch,
            1.2 * inch,
            1.2 * inch,
            1.2 * inch,
        ]
        table = Table(data, rowHeights=20, repeatRows=1, colWidths=c_width)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        return table

    def create_canvas_fig(self, fig, doc):
        # Crear un objeto de lienzo de Matplotlib para la figura
        imgdata = BytesIO()

        fig.savefig(imgdata, format="svg")
        imgdata.seek(0)  # rewind the data

        drawing = svg2rlg(imgdata)
        return drawing

    def create_doc(self, doc):
        tableHeader_paragraph = Paragraph("Tabla de datos", styles["Heading2"])
        plotsHeader_paragraph = Paragraph("Datos en forma gráfica", styles["Heading2"])
        dataHeader_paragraph = Paragraph("Datos resumidos", styles["Heading2"])

        init_par = Paragraph(
            f"En este informe se recogen los últimos días de la actividad {self.exercise} de {self.user}. A continuación, se presenta en forma de tabla los datos recogidos por dias.",
            styles["Normal"],
        )
        table = doc.create_table(self.data)
        stats, plot_left, plot_right = self.get_statistics()
        img_left = self.create_canvas_fig(plot_left, doc)
        img_right = self.create_canvas_fig(plot_right, doc)
        stats_paragraph = Paragraph(stats, styles["Normal"])
        doc_organization = [
            tableHeader_paragraph,
            init_par,
            self.space,
            table,
            self.space,
            plotsHeader_paragraph,
            self.space,
            img_left,
            self.space,
            img_right,
            self.space,
            dataHeader_paragraph,
            stats_paragraph,
        ]
        doc.build(doc_organization)
