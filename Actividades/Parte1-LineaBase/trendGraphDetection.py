import rrdtool
from Notify import sendAlertAttached
import time

# Globales
RRD_PATH = "RRD/"
IMG_PATH = "IMG/"

if __name__ == "__main__":
    ultima_lectura = int(rrdtool.last(RRD_PATH + "trend.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 600

    ret = rrdtool.graphv(
        IMG_PATH + "deteccion.png",
        "--start", str(tiempo_inicial),
        "--end", str(tiempo_final),
        "--vertical-label=Cpu load",
        '--lower-limit', '0',
        '--upper-limit', '100',
        "--title=Cagra del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",

        "DEF:cargaCPU=" + RRD_PATH + "trend.rrd:CPUload:AVERAGE",

        "VDEF:cargaMAX=cargaCPU,MAXIMUM",
        "VDEF:cargaMIN=cargaCPU,MINIMUM",
        "VDEF:cargaSTDEV=cargaCPU,STDEV",
        "VDEF:cargaLAST=cargaCPU,LAST",
        
        # "CDEF:cargaEscalada=cargaCPU,8,*",
        # Example A, B, C, IF as if (A) then (B) else (C)
        "CDEF:umbral5=cargaCPU,5,LT,0,cargaCPU,IF",
        "CDEF:umbral10=cargaCPU,10,LT,0,cargaCPU,IF",
        "AREA:cargaCPU#00FF00:Carga del CPU",
        "AREA:umbral5#FF9F00:Carga CPU mayor que 5",
        "HRULE:15#FF0000:Umbral 1 - 5%",
        "AREA:umbral10#FF0000:Carga CPU mayor que 10",
        "HRULE:15#FF0000:Umbral 5 - 10%",

        "PRINT:cargaLAST:%6.2lf",
        "GPRINT:cargaMIN:%6.2lf %SMIN",
        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
        "GPRINT:cargaLAST:%6.2lf %SLAST"
    )

    print(ret)

    ultimo_valor = float(ret["print[0]"])
    if ultimo_valor > 4:
        sendAlertAttached("Sobrepasa Unmbral línea base")
        print("Sobrepasa Unmbral línea base")
