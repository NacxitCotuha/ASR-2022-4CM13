import rrdtool

if __name__ == "__main__":
    ret = rrdtool.create(
        "RRD/trend.rrd",
        "--start", "N",
        "--step", "60", #"--step", "300", # para la practica
        "DS:CPUload:GAUGE:600:0:100", #"DS:CPUload:GAUGE:600:U:U,
        "RRA:AVERAGE:0.5:1:24"# Para la practica debe ser mayor a 24
    )

    if ret:
        print(rrdtool.error())