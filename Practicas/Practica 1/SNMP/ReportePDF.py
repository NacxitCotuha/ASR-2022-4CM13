import os

from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
#A4 : width (ancho) = 595.2, height (alto) = 841.8,

NAME_FILE = "ReporteSNMP"
PATH = "Reportes"


def crear_reporte():
    if os.path.exists(PATH):
        crear_reporte_pdf()
    else:
        print(f"Se ha Creado la carpeta: {PATH}")
        os.mkdir(PATH)
        crear_reporte_pdf()


def crear_reporte_pdf() -> None:
    fecha = datetime.today().strftime("%Y-%m-%d-%H-%M")
    path_complete_file = f"{PATH}/{NAME_FILE}-{fecha}.pdf"
    # No es necesario el A4 por ser Default
    ancho, alto = A4
    reporte = canvas.Canvas(path_complete_file, pagesize=A4) 
    text = reporte.beginText(50, alto - 50)
    text.setFont("Times-Roman", 20)
    text.textLine("Reporte SNMP")
    text.textLine(fecha)
    text.setFont("Times-Roman", 12)
    text.textLine("Reporte SNMP")
    text.textLine(fecha)
    reporte.drawText(text)
    reporte.save()

if __name__ == "__main__":
    crear_reporte()