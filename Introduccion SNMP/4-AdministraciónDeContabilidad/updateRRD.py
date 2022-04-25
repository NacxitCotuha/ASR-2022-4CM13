import time
import rrdtool
from getSNMP import consultarSNMP

if __name__ == "__main__":
    while True:
        tcp_in_segments = int(
            consultarSNMP('comunidadASR', 'localhost',
                         '1.3.6.1.2.1.6.10.0'))
        tcp_out_segments = int(
            consultarSNMP('comunidadASR', 'localhost',
                         '1.3.6.1.2.1.6.11.0'))

        valor = "N:" + str(tcp_in_segments) + ':' + str(tcp_out_segments)
        print(valor)
        rrdtool.update('segmentosRed.rrd', valor)
        # rrdtool.dump('traficoRED.rrd','traficoRED.xml')
        time.sleep(1)

    if ret:
        print(ret)
        time.sleep(300)
