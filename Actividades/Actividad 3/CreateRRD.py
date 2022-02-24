import rrdtool

if __name__ == '__main__':
    ret = rrdtool.create(
        "traficoRED.rrd",
        "--start",'N',
        "--step",'60',
        "DS:segmentosEntrada:COUNTER:600:U:U",
        "DS:segmentosSalida:COUNTER:600:U:U",
        "RRA:AVERAGE:0.5:6:5",
        "RRA:AVERAGE:0.5:1:20"
    )

    if ret:
        print(rrdtool.error())