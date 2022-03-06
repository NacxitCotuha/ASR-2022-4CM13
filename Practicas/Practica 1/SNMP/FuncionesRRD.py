import codecs
import os
from re import ASCII
import sys
from time import time
import threading
import time
import rrdtool
from pysnmp.hlapi import *

PATH_RRD = "RRD"
PATH_IMG = "PNG"

MODULOS = {
    1: "Multicast", #ifInNUcastPkts  12: Paquetes multicast que ha recibido una interfaz 
    2: "IPv4", # ipInReceives { ip 9 }: Paquetes recibidos exitosamente, entregados a protocolos IPv4
    3: "ICMP", # icmpOutEchoReps { icmp 22 }: Mensajes de respuesta ICMP que ha enviado el agente
    4: "Octetos", # tcpOutSegs { tcp 11 }: Segmentos enviados, incluyendo los de las conexiones actuales pero excluyendo los que contienen solamente octetos retransmitidos
    5: "UDP" # udpInErrors { udp 3 }: Datagramas recibidos que no pudieron ser entregados por cuestiones distintas a la falta de aplicación en el puerto destino 
}


def hex_to_string( dato ) -> str:
    string_hex = dato[2:]
    bytes_obj = bytes.fromhex(string_hex)
    try:
        string = bytes_obj.decode()
    except:
        try:
            string = bytes_obj.decode('ISO-8859-1')
        except:
            string = bytes_obj.decode('windows-1252')
    return string


def consulta_snmp(comunidad: str, host: str, oid: str, version: int):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(
            SnmpEngine(),
            CommunityData(comunidad, mpModel=version), # 0 = SNMPv1, 1 = SNMPv2
            UdpTransportTarget((host, 161)),
            ContextData(), 
            ObjectType(ObjectIdentity(oid))
        )
    )
    if errorIndication and not (errorIndication == "No SNMP response received before timeout"):
        print(errorIndication)
    elif errorStatus:
        print(f"{errorStatus} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
    else:
        for varBind in varBinds:
            # varB=(" = ".join([x.prettyPrint() for x in varBind]))
            # resultado = varB.split()[2]
            try:
                varB=(" = ".join([x.prettyPrint() for x in varBind]))
                valor = varB.split()[2]
                if valor[:2] == "0x":
                    resultado = hex_to_string(valor)
                    #print(type(resultado))
                else:
                    resultado = valor
            except:
                varB=(" = ".join([x.prettyPrint() for x in varBind]))
                string_hex = varB.split(" = ", maxsplit=2)[1]
                if string_hex[:2] == "0x":
                    resultado = hex_to_string(string_hex)
                else:
                    hex_string = varB
                    bytes_obj = hex_string.encode()
                    resultado = bytes_obj.decode("UTF-8")
        return resultado


def crear_path_rrd(host:str, comunidad: str, ver: int) -> str:
    if not os.path.isdir(PATH_RRD):
        os.mkdir(PATH_RRD)
    return f"{PATH_RRD}/{host}_{comunidad}_Version{ver + 1}.rrd"


def crear_path_img(host:str, comunidad: str, ver: int, modulo: str) -> str:
    if not os.path.isdir(PATH_IMG):
        os.mkdir(PATH_IMG)
    return f"{PATH_IMG}/{host}_{comunidad}_Version{ver + 1}_{modulo}.png"


def create_rrd(path: str) -> None:
    print(f"Creando el archivo: {path}...")
    ret = rrdtool.create(
        path,
        "--start", "N",
        "--step", "60",
        f"DS:segmentos_{MODULOS[1]}:COUNTER:600:U:U",
        f"DS:segmentos_{MODULOS[2]}:COUNTER:600:U:U",
        f"DS:segmentos_{MODULOS[3]}:COUNTER:600:U:U",
        f"DS:segmentos_{MODULOS[4]}:COUNTER:600:U:U",
        f"DS:segmentos_{MODULOS[5]}:COUNTER:600:U:U",
        "RRA:AVERAGE:0.5:6:5",
        "RRA:AVERAGE:0.5:1:20"
    )

    if ret:
        print(rrdtool.error())
    print(f"El archivo: {path} fue creado")
    return


def update_rrd(path: str, comunidad: str, host: str, version: int, inter: int) -> None:
    while True:
        ifInNUcastPkts = consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.12.{inter}", version=version)
        ipInReceives = consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.4.9.0", version=version)
        icmpOutEchoReps = consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.5.22.0", version=version)
        tcpOutSegs = consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.6.11.0", version=version)
        udpInErrors = consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.7.3.0", version=version)
        valor = f"N:{str(ifInNUcastPkts)}:{str(ipInReceives)}:{str(icmpOutEchoReps)}:{str(tcpOutSegs)}:{str(udpInErrors)}"
        # print(valor)
        ret = rrdtool.update(path, valor)
        time.sleep(1)
        if ret:
            print(rrdtool.error())
            time.sleep(30)


def generar_all_rrd(comunidad: str, host: str, version: int, interface: int) -> None:
    path_rrd = crear_path_rrd(host=host, comunidad=comunidad, ver=version, )
    if not os.path.isfile(path=path_rrd):
        create_rrd(path=path_rrd)
    demonio_update = threading.Thread(target=update_rrd, args=(path_rrd, comunidad, host, version, interface,), daemon=True)
    print(f"Iniciando nuevo demonio para: {host}, {comunidad}, Ver{version + 1}" )
    demonio_update.start()
    # update_rrd(path=path_rrd, comunidad=comunidad, host=host, version=version, inter=interface)
    return


def graficar_rrd(comunidad: str, host: str, version: int) -> tuple[str, str, str, str, str]:
    tiempo_actual = int(time.time())
    # Grafica desde el tiempo actual menos diez minutos 
    tiempo_inicial = tiempo_actual - 1800
    path_rrd = crear_path_rrd(host=host, comunidad=comunidad, ver=version)
    path_img1 = crear_path_img(host=host, comunidad=comunidad, ver=version, modulo=MODULOS[1])
    ret1 = rrdtool.graph(
        path_img1,
        "--start",str(tiempo_inicial),
        "--end","N",
        "--vertical-label=Segmentos",
        "--title=Paquetes multicast que ha recibido una interfaz",
        f"DEF:Datos={path_rrd}:segmentos_{MODULOS[1]}:AVERAGE",
        "AREA:Datos#00FF00:Tráfico de entrada",
        "LINE3:Datos#0000FF:Tráfico de salida"
    )
    path_img2 = crear_path_img(host=host, comunidad=comunidad, ver=version, modulo=MODULOS[2])
    ret2 = rrdtool.graph(
        path_img2,
        "--start",str(tiempo_inicial),
        "--end","N",
        "--vertical-label=Segmentos",
        "--title=Paquetes recibidos exitosamente,\nentregados a protocolos IP",
        f"DEF:Datos={path_rrd}:segmentos_{MODULOS[2]}:AVERAGE",
        "AREA:Datos#00FF00:Tráfico de entrada",
        "LINE3:Datos#0000FF:Tráfico de salida"
    )
    path_img3 = crear_path_img(host=host, comunidad=comunidad, ver=version, modulo=MODULOS[3])
    ret3 = rrdtool.graph(
        path_img3,
        "--start",str(tiempo_inicial),
        "--end","N",
        "--vertical-label=Segmentos",
        "--title=Mensajes de respuesta ICMP que ha enviado el agente",
        f"DEF:Datos={path_rrd}:segmentos_{MODULOS[3]}:AVERAGE",
        "AREA:Datos#00FF00:Tráfico de entrada",
        "LINE3:Datos#0000FF:Tráfico de salida"
    )
    path_img4 = crear_path_img(host=host, comunidad=comunidad, ver=version, modulo=MODULOS[4])
    ret4 = rrdtool.graph(
        path_img4,
        "--start",str(tiempo_inicial),
        "--end","N",
        "--vertical-label=Segmentos",
        "--title=Segmentos enviados, \nincluyendo los de las conexiones actuales \npero excluyendo los que contienen solamente \noctetos retransmitidos",
        f"DEF:Datos={path_rrd}:segmentos_{MODULOS[4]}:AVERAGE",
        "AREA:Datos#00FF00:Tráfico de entrada",
        "LINE3:Datos#0000FF:Tráfico de salida"
    )
    path_img5 = crear_path_img(host=host, comunidad=comunidad, ver=version, modulo=MODULOS[5])
    ret5 = rrdtool.graph(
        path_img5,
        "--start",str(tiempo_inicial),
        "--end","N",
        "--vertical-label=Segmentos",
        "--title=Datagramas recibidos que no pudieron ser entregados \npor cuestiones distintas a la falta de \naplicación en el puerto destino",
        f"DEF:Datos={path_rrd}:segmentos_{MODULOS[5]}:AVERAGE",
        "AREA:Datos#00FF00:Tráfico de entrada",
        "LINE3:Datos#0000FF:Tráfico de salida"
    )

    return (path_img1, path_img2, path_img3, path_img4, path_img5)






if __name__ == "__main__":
    host = "localhost"
    generar_all_rrd(
        comunidad="comunidadKaliSNMP",
        host="localhost",
        version=0,
        interface=6,
    )

    generar_all_rrd(
        comunidad="comunidadKali",
        host="localhost",
        version=0,
        interface=6,
    )

    time.sleep(56)
    graficar_rrd(comunidad="comunidadKaliSNMP", host=host, version=0)
    graficar_rrd(comunidad="comunidadKali", host=host, version=0)
    sys.exit()