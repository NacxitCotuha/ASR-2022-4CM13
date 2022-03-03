import os
import rrdtool


PATH = "RRD"


def crear_rrd(nombre_agente: str):
    if not os.path.exists(PATH):
        print(f"Se ha creado la carpeta: {PATH}")
        os.mkdir(PATH)
    path_complete_file: str = f"{PATH}/{nombre_agente}.rrd"
    ret = rrdtool.create(
        path_complete_file,
    )