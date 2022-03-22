import os
import time

# SNMP Libraries
import rrdtool
from pysnmp.hlapi import *

# Constantes
DIRECTORY_RRD = "RRD"
DIRECTORY_XML = "XML"
MODULES = {
    1: "tcpConnState",
    2: "tcpConnLocalDireccion",
    3: "tcpConnLocalPort",
    4: "tcpConnRemAddress",
    5: "tcpConnRemPort",
}

def hexToString( cadena ) -> str:
    string: str
    string_hex = cadena[2:]
    bytes_obj = bytes.fromhex(string_hex);
    try:
        string = bytes_obj.decode()
    except UnicodeDecodeError as error_utf:
        try:
            string = bytes_obj.decode("ISO-8859-1")
        except UnicodeDecodeError as error_iso:
            string = bytes_obj.decode("windows-1252")
    return string


def crearPathRRD( host: str, comunidad: str ) -> str:
    if not os.path.isdir(DIRECTORY_RRD):
        os.mkdir(DIRECTORY_RRD)
    return f"{DIRECTORY_RRD}/{host}_{comunidad}.rrd"


def crearPathXML( host: str, comunidad: str ) -> str:
    if not os.path.isdir(DIRECTORY_XML):
        os.mkdir(DIRECTORY_XML)
    return f"{DIRECTORY_XML}/{host}_{comunidad}"


def consultaSNMP( comunidad: str, host: str, oid: str ) -> (any | str):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(
            SnmpEngine(),
            CommunityData(communityName=comunidad, mpModel=0), # SNMPv1 = 0, SNMPv2 = 1
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
        for var_bind in var_binds:
            var_b = (" = ".join([x.prettyPrint() for x in var_bind]))
            valor = var_b.split()[2]
            if valor[:2] == "0x":
                resultado = hexToString(valor)
            else:
                resultado = valor
        return resultado


def crearRRD( path: str ) -> None:
    print(f"Creando el archivo: {path}")
    ret = rrdtool.create(
        "--start", "N",
        "--step", "60",
        f"DS:segmento_{MODULES[1]}:COUNTER:600:U:U",
        f"DS:segmento_{MODULES[2]}:COUNTER:600:U:U",
        f"DS:segmento_{MODULES[3]}:COUNTER:600:U:U",
        f"DS:segmento_{MODULES[4]}:COUNTER:600:U:U",
        f"DS:segmento_{MODULES[5]}:COUNTER:600:U:U",
        "RRA:AVERAGE:0.5:6:5",
        "RRA:AVERAGE:0.5:1:20"
    )
    if ret:
        print(rrdtool.error)
    print(f"El archivo: {path} fue creado")


def updateRRD( path_rrd: str, comunidad: str, host: str ) -> None:
    path_xml = crearPathXML(host=host, comunidad=comunidad)
    while True:
        tcpConnState = consultaSNMP()
        tcpConnLocalDireccion = consultaSNMP()
        tcpConnLocalPort = consultaSNMP()
        tcpConnRemAddress = consultaSNMP()
        tcpConnRemPort = consultaSNMP()
        datos_rrd = f"N:{tcpConnState}:{tcpConnLocalDireccion}:{tcpConnLocalPort}:{tcpConnRemAddress}:{tcpConnRemPort}"
        rrdtool.update(path_rrd, datos_rrd)
        rrdtool.dump(path_rrd, path_xml)
        time.sleep(30)


def generarThreadRDD( comunidad: str, host: str ) -> None:
    path_rrd = crearPathRRD(host=host, comunidad=comunidad)
    if not os.path.isfile(path=path_rrd):
        crearRRD(path=path_rrd)
    rrd_thread = 12