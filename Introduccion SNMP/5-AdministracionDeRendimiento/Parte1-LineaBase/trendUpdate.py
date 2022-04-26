import time
import rrdtool
from getSNMP import consultarSNMP

RRD_PATH = "RRD/"
carga_cpu = 0

if __name__ == "__main__":
    while True:
        carga_cpu = int(consultarSNMP('comunidadKali','localhost','1.3.6.1.2.1.25.3.3.1.2.196608'))
        valor = "N:" + str(carga_cpu)
        print(valor)
        rrdtool.update(RRD_PATH + "trend.rrd", valor)
        rrdtool.dump(RRD_PATH + "trend.rrd", "trend.xml")
        time.sleep(5) #time.sleep(1)