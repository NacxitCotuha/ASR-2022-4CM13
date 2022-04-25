import os

# RRD Librerias
import rrdtool
from pysnmp.hlapi import *

# Constante
DIRECTORY_RRD = "RRD"
DIRECTORY_XML = "XML"
MODULES_NAME = {}


def hexToString( cadena: str ) -> str:
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


def pathRRD( host: str, comunidad: str ) -> str:
    if not os.path.isdir(DIRECTORY_RRD):
        os.mkdir(DIRECTORY_RRD)
    return f"{DIRECTORY_RRD}/{host}_{comunidad}.rrd"


def pathXML( host: str, comunidad: str ) -> str:
    if not os.path.isdir(DIRECTORY_XML):
        os.mkdir(DIRECTORY_XML)
    return f"{DIRECTORY_XML}/{host}_{comunidad}.xml"


def consultaSNMP( comunidad: str, host: str, oid: str) -> any:
    error_indication, error_status, error_index, var_binds = next(
        getCmd(
            SnmpEngine(),
            CommunityData(comunidad),
            UdpTransportTarget((host, 162)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        )
    )
    if error_indication:
        print(error_indication)
    elif error_status:
        print(f"{error_status} at {error_index and var_binds[int(error_index) - 1][0] or '?'}")
    else:
        resultado: any = ""
        for var_bind  in var_binds:
            aux_var_bind = (" = ".join([x for x in var_bind]))
            valor = aux_var_bind.split()[2]
            if valor[:2] == "0x":
                resultado = hexToString(valor)
            else:
                resultado = valor
        return resultado


def crearRRD( path: str ) -> None:
    print(f"Creando el archivo.rrd en {path}")
    ret = rrdtool.create(
        path, "--start", "N", "--step", "60",
        f"DS:segmento_{MODULES_NAME[]}:GAUGE:600:U:U",
        "RRA:AVERAGE:0.5:1:24"
    )