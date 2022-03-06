# Funciones de la practica
import FuncionesRRD
# Librerias Python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
# Una hoja A4 está constituida por 595.2 puntos de ancho (width) y 841.8 puntos de alto (height).

PATH_PDF = "ReportesPDF"

def create_path_pdf(host: str, comunidad: str, ver: int) -> str:
    if not os.path.isdir(PATH_PDF):
        os.mkdir(PATH_PDF)
    return f"{PATH_PDF}/{host}_{comunidad}_Version{ver + 1}.pdf"



def crear_pdf(host: str, comunidad: str, ver: int, system: str | None, fecha: str) -> None:
    path_pdf = create_path_pdf(host=host, comunidad=comunidad, ver=ver)
    # Elminamos el archivo por cualquier cosa
    eliminar_pdf(path=path_pdf)
    # Genera el archivo
    c = canvas.Canvas(path_pdf, pagesize=A4)
    width, height = A4
    # Logo
    if system:
        interfaces = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid="1.3.6.1.2.1.2.1.0", version=ver)
        sysContact = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid="1.3.6.1.2.1.1.4.0", version=ver)
        sysName = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid="1.3.6.1.2.1.1.5.0", version=ver)
        sysLocation = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid="1.3.6.1.2.1.1.6.0", version=ver)
        sysInfo = "Linux" if ("Linux" in system) else "Windows"
        path_logo = "LOGO/logo_linux.png" if ("Linux" in system) else "LOGO/logo_windows.png"
    else:
        path_logo = "LOGO/logo_otro.png"
        sysInfo = "No Info"
        interfaces = "No Info"
        sysContact = "No Info"
        sysName = "No Info"
        sysLocation = "No Info"
    c.drawImage(image=path_logo, x=50, y=int(height - 100), width=50, height=50)
    # Textos Encabezados
    text = c.beginText(x=110, y=int(height - 74))
    text.setFont("Times-Roman", 24)
    text.textLine(f"Reporte PDF {fecha}")
    # -> info
    text.setFont("Times-Roman", 12)
    text.textLine(f"HOST/IP: {host}")
    text.textLine(f"Comunidad: {comunidad}")
    text.textLine(f"Version: {ver + 1}")
    text.textLine(f"System Info: {sysInfo}")
    text.textLine(f"Contacto: {sysContact}")
    text.textLine(f"Nombre: {sysName}")
    text.textLine(f"Ubicacion: {sysLocation}")
    text.textLine(f"Interfaces: {interfaces}")
    c.drawText(text)
    if system:
        img1, img2, img3, img4, img5 = FuncionesRRD.graficar_rrd(comunidad=comunidad, host=host, version=ver)
        width_img = 480
        height_img = 240
        c.drawImage(image=img1, x=50, y=int(height - (50 + 2*height_img)), width=width_img, height=height_img)
        c.drawImage(image=img2, x=50, y=int(height - (50 + 3*height_img)), width=width_img, height=height_img)
        c.showPage()
        # Nueva Pagina
        c.drawImage(image=img3, x=50, y=int(height - (50 + height_img)), width=width_img, height=height_img)
        c.drawImage(image=img4, x=50, y=int(height - (50 + 2*height_img)), width=width_img, height=height_img)
        c.drawImage(image=img5, x=50, y=int(height - (50 + 3*height_img)), width=width_img, height=height_img)
    #c.showPage()
    #c.drawImage(image=path_logo, x=50, y=int(height - 100), width=50, height=50)
    c.save()
    print(f"El Archivo: {path_pdf} se ha generado\n")
    return

def eliminar_pdf(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)
    return


if __name__ == "__main__":
    crear_pdf(host="localhost", comunidad="comunidadKaliSNMP", ver=0, system="Soy Linux", fecha="HOY")
    crear_pdf(host="localhost", comunidad="comunidadKali", ver=0, system="Soy Windows", fecha="HOY")
    crear_pdf(host="192.168.0.4", comunidad="comunidadSNMP", ver=0, system=None, fecha="HOY")
