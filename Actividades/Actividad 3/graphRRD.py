import sys
import rrdtool
import time
tiempo_actual = int(time.time())

#Grafica desde el tiempo actual menos diez minutos

tiempo_inicial = tiempo_actual - 1000


ret = rrdtool.graph( 
    "Segmentos.png",
    "--start",str(tiempo_inicial),
    "--end","N",
    "--vertical-label=Segmentos",
    "--title=Segmentos TCP de un agente \n Usando SNMP y RRDtools",
    "DEF:SegEntrada=traficoRED.rrd:segmentosEntrada:AVERAGE",
    "DEF:SegSalida=traficoRED.rrd:segmentosSalida:AVERAGE",
    "AREA:SegEntrada#00FF00:Tráfico de entrada",
    "LINE3:SegSalida#0000FF:Tráfico de salida")