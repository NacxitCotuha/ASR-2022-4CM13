import rrdtool


class ServicioSNMP:
    def __init__(self, comunidad) -> None:
        self._comunidad = comunidad
        pass


def create_rrd():
    ret = rrdtool.create(
        f".rrd",
        "--start", "N",
        "--step", "60",
        f"DS:{}In:COUNTER:600:U:U",
        f"DS:{}Out:COUNTER:600:U:U",
        "RRA:AVERAGE:0.5:6:5",
        "RRA:AVERAGE:0.5:1:20"
    )

    if ret:
        print(rrdtool.error())


def get_snmp():