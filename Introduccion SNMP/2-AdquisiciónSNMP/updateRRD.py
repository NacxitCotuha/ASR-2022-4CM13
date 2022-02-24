from ast import arg
import time
import rrdtool
from getSNMP import consultarSNMP

if __name__ == '__main__':
    while 1:
        total_input_traffic = int(
            consultarSNMP(
                'comunidadSNMP',
                'localhost',
                '1.3.6.1.2.1.2.2.1.10.6'
            )
        )

        total_output_traffic = int(
            consultarSNMP(
                'comunidadSNMP',
                'localhost',
                '1.3.6.1.2.1.2.2.1.16.6'
            )
        )

        valor = f"N:{str(total_input_traffic)}:{str(total_output_traffic)}"
        print(valor)
        rrdtool.update('traficoRED.rrd', valor)
        rrdtool.dump("traficoRED.rrd", "traficoRED.xml")
        time.sleep(1)
    
    if ret:
        print(rrdtool.error())
        time.sleep(30)