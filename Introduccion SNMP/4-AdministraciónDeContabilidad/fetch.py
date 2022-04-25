import rrdtool

RRD_FILE = "segmentosRed.rrd"
XML_FILE = "segmentosRed.xml"

if __name__ == "__main__":
    last_update = rrdtool.lastupdate(RRD_FILE)
    # Grafica desde la última lectura menos cinco minutos
    print(last_update)
    tiempo_inicial = int(last_update['date'].timestamp()) - 300
    print(f"Tiempo Inicial = {tiempo_inicial}")
    rrdtool.dump(RRD_FILE, XML_FILE)
    result = rrdtool.fetch(RRD_FILE, "-s", str(tiempo_inicial), "LAST")
    start, end, step = result[0]
    ds = result[1]
    rows = result[2]
    print(result)
    print(ds)
    print(rows)