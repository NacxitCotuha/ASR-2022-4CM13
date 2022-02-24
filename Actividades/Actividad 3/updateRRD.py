from ast import arg
import time
import rrdtool
from getSNMP import consultarSNMP

if __name__ == '__main__':
    while 1:
        tcp_in_segment = int(
            consultarSNMP(
                'comunidadSNMP',
                'localhost',
                '1.3.6.1.2.1.6.10.0'
            )
        )

        tcp_out_segment = int(
            consultarSNMP(
                'comunidadSNMP',
                'localhost',
                '1.3.6.1.2.1.6.11.0'
            )
        )

        valor = f"N:{str(tcp_in_segment)}:{str(tcp_out_segment)}"
        print(valor)
        rrdtool.update('traficoRED.rrd', valor)
        # rrdtool.dump("traficoRED.rrd", "traficoRED.xml")
        time.sleep(1)
    
    if ret:
        print(rrdtool.error())
        time.sleep(30)