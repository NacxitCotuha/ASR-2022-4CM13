import os
import time

# RRD libraries
import rrdtool
from pysnmp.hlapi import *


# Constantes
DIRECTORY_RRD = "RRD"
DIRECTORY_XML = "XML"
MODULES_HTTP = {
    1: "tcpConnState",
    2: "tcpConnLocalDireccion",
    3: "tcpConnLocalPort",
    4: "tcpConnRemAddress",
    5: "tcpConnRemPort",
    10: "tcpInSegs",
    11: "tcpOutSegs"
}

def hexToString( cadena ) -> str:
    string: str
    string_hex = cadena[2:]
    bytes_object = bytes.fromhex(string_hex)
    try:
        string = bytes_object.decode()
    except UnicodeDecodeError:
        try:
            string = bytes_object.decode("ISO-8859-1")
        except UnicodeDecodeError:
            string = bytes_object.decode("windows-1252")
    return string


def crearPathRRD( host: str, comunidad: str ) -> str:
    if not os.path.isdir(DIRECTORY_RRD):
        os.mkdir(DIRECTORY_RRD)
    return f"{DIRECTORY_RRD}/{host}_{comunidad}.rrd"


def crearPathXML( host: str, comunidad: str ) -> str:
    if not os.path.isdir(DIRECTORY_XML):
        os.mkdir(DIRECTORY_XML)
    return f"{DIRECTORY_XML}/{host}_{comunidad}.xml"


def consultaSNMP( comunidad: str, host: str, oid: str ) ->  any:
    error_indication, error_status, error_index, var_binds = next(
        getCmd(
            SnmpEngine(),
            CommunityData(comunidad, mpModel=0), # SNMPv1 = 0, SNMPv2 = 1
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
    )
    if error_indication and not (error_indication == "No SNMP response received before timeout"):
        print(error_indication)
    elif error_status:
        print(f"{error_status} at {error_index and var_binds[int(error_index) - 1][0] or '?'}")
    else:
        resultado: any = 0
        for var_bind in var_binds:
            var_b = (" = ".join([x.prettyPrint() for x in var_bind]))
            valor = var_b.split()[2]
            if valor[:2] == "0x":
                resultado = hexToString(valor)
            else:
                resultado = valor
        return resultado


def crearRRD( path: str ) -> None:
    print(F"Creando el archivo: {path}")
    ret = rrdtool.create(
        path,
        "--start", "N",
        "--step", "60",
        f"DS:seg_{MODULES_HTTP[10]}:COUNTER:120:U:U",
        f"DS:seg_{MODULES_HTTP[11]}:COUNTER:120:U:U",
        "RRA:LAST:0.5:6:5",
        "RRA:LAST:0.5:1:20"
    )
    if ret:
        print(rrdtool.error())
    print(f"El archivo: {path} fue creado")


def updateRRDHTTP( path_rrd: str, comunidad: str, host: str ) -> None:
    path_xml = crearPathXML(host=host, comunidad=comunidad)
    intentos_consultas: int = 0
    while intentos_consultas < 5:
        is_up = consultaSNMP(comunidad=comunidad, host=host, oid="1.3.6.1.2.1.1.3.0")
        if is_up:
            intentos_consultas = 0
            tcpInSegs = consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.6.10.0")
            tcpOutSegs = consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.6.11.0")
            datos_rrd = f"N:{tcpInSegs}:{tcpOutSegs}"
            rrdtool.update(path_rrd, datos_rrd)
            rrdtool.dump(path_rrd, path_xml)
            time.sleep(30)
        else:
            intentos_consultas = intentos_consultas + 1
    else:
        print(f"No se puede conectar con {host} {comunidad}")


def promedioRRD( host: str, comunidad: str ) -> tuple[ int, int, float, float]:
    suma_1: float = 0
    suma_2: float = 0
    contador: int = 0
    path_rrd = crearPathRRD(host=host, comunidad=comunidad)
    last_update = rrdtool.lastupdate(path_rrd)
    # Grafica desde la  lectura de hace un minuto y menos cinco minutos
    tiempo_inicial = int(last_update['date'].timestamp()) - 360
    tiempo_final = int(last_update['date'].timestamp()) - 60
    datos = rrdtool.fetch(path_rrd, "LAST", "-s", str(tiempo_inicial), "-e", str(tiempo_final))
    start, end, stop = datos[0]
    ds = datos[1]
    rows = datos[2]
    for row in rows:
        dato_1, dato_2 = row
        if (dato_1 is None) and (dato_2 is None):
            continue
        suma_1 = suma_1 + dato_1
        suma_2 = suma_2 + dato_2
        contador = contador + 1
    if contador == 0:
        return tiempo_inicial, tiempo_final, 0.0, 0.0
    else:
        return start, end, ( suma_1 / contador), suma_2 / contador


def fetchRRD( path_rrd: str ):
    last_update = rrdtool.lastupdate(path_rrd)
    # Grafica desde la última lectura menos cinco minutos
    tiempo_inicial  = int(last_update['date'].timestamp()) - 300
    print(f"Tiempo inicial: {tiempo_inicial}")
    result = rrdtool.fetch(path_rrd, "LAST", "-s", str(tiempo_inicial))
    start, end, stop = result[0]
    ds = result[1]
    rows = result[2]
    print(result)
    print(ds)
    print(rows)
    print(len(rows))



