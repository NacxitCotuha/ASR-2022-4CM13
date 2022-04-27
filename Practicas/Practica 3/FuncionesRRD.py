import os
import time

# RRD Librerias
import rrdtool
from pysnmp.hlapi import *

# Extras Librerias 
from FuncionesExtras import *

def pathRRD( host: str, comunidad: str ) -> str:
    if not os.path.isdir(DIRECTORY_RRD):
        os.mkdir(DIRECTORY_RRD)
    return f"{DIRECTORY_RRD}/{host}_{comunidad}.rrd"


def pathXML( host: str, comunidad: str ) -> str:
    if not os.path.isdir(DIRECTORY_XML):
        os.mkdir(DIRECTORY_XML)
    return f"{DIRECTORY_XML}/{host}_{comunidad}.xml"


def pathIMG( host: str, comunidad: str, modulo: str ) -> str:
    if not os.path.isdir(DIRECTORY_IMG):
        os.mkdir(DIRECTORY_IMG)
    return f"{DIRECTORY_IMG}/{host}_{comunidad}_{modulo}.png"


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
        path, "--start", "N", 
        "--step", "300",
        f"DS:{MODULES_NAME[0]}:GAUGE:600:U:U",
        f"DS:{MODULES_NAME[1]}:GAUGE:600:U:U",
        f"DS:{MODULES_NAME[2]}:GAUGE:600:U:U",
        "RRA:AVERAGE:0.5:1:48"
    )
    if ret:
        print(rrdtool.error())


def updateRRD( comunidad: str, host: str, path_rrd: str, path_xml: str ) -> None:
    carga_cpu = 0
    carga_ram = 0
    carga_stg = 0
    while True:
        carga_cpu = int(consultaSNMP(comunidad=comunidad, host=host, oid="1.3.6.1.2.1.25.3.3.1.2.196608"))
        carga_ram = int(consultaSNMP(comunidad=comunidad, host=host, oid="1.3.6.1.2.1.25.2.3.1.5."))
        carga_stg = int(consultaSNMP(comunidad=comunidad, host=host, oid=""))
        valor = f"N:{str(carga_cpu)}:{carga_ram}:{carga_stg}"
        print(valor)
        rrdtool.update(path_rrd, valor)
        rrdtool.dump(path_rrd, path_xml)
        time.sleep(5)


def graphDetection( path_rrd: str, path_cpu: str, path_ram: str, path_hdd: str ) -> None:
    ultima_lectura = int(rrdtool.last(path_rrd))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 300
    carga_cpu_img = rrdtool.graphv(
        path_cpu,
        "--start", str(tiempo_inicial),
        "--end", str(tiempo_final),
        "--vertical-label=Cpu load",
        '--lower-limit', '0',
        '--upper-limit', '100',
        "--title=Carga del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",

        f"DEF:{MODULES_NAME[0]}={path_rrd}:{MODULES_NAME[0]}:AVERAGE",

        f"VDEF:cargaMAX={MODULES_NAME[0]},MAXIMUM",
        f"VDEF:cargaMIN={MODULES_NAME[0]},MINIMUM",
        f"VDEF:cargaSTDEV={MODULES_NAME[0]},STDEV",
        f"VDEF:cargaLAST={MODULES_NAME[0]},LAST",
        
        #Umbrales
        # Umbral 20%
        f"CDEF:umbral20={MODULES_NAME[0]},20,LT,0,{MODULES_NAME[0]},IF",
        f"AREA:{MODULES_NAME[0]}#00FFFF:Carga del CPU", # aqua
        f"AREA:umbral20#7FFFD4:Carga CPU mayor que 20%", # aquamarine
        f"HRULE:15#0000FF:Umbral 20%", # Azul
        # Umbral 50%
        f"CDEF:umbral50={MODULES_NAME[0]},50,LT,0,{MODULES_NAME[0]},IF",
        f"AREA:{MODULES_NAME[0]}#ADFF2F:Carga del CPU", # greenyellow
        f"AREA:umbral50#9ACD32:Carga CPU mayor que 50%", # yellowgreen
        f"HRULE:15#00FF00:Umbral 50%", # Verde
        # Umbral 90%
        f"CDEF:umbral90={MODULES_NAME[0]},90,LT,0,{MODULES_NAME[0]},IF",
        f"AREA:{MODULES_NAME[0]}#FFA500:Carga del CPU", # orange
        f"AREA:umbral90#FF4500:Carga CPU mayor que 90%", # orangered
        f"HRULE:15#FF0000:Umbral 90%", # Rojo

        "PRINT:cargaLAST:%6.2lf",
        "GPRINT:cargaMIN:%6.2lf %SMIN",
        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
        "GPRINT:cargaLAST:%6.2lf %SLAST"
    )

    carga_ram_img = rrdtool.graphv(
        path_ram,
        "--start", str(tiempo_inicial),
        "--end", str(tiempo_final),
        "--vertical-label=RAM Load",
        '--lower-limit', '0',
        '--upper-limit', ' 16777216',
        "--title=Carga de la RAM del agente Usando SNMP y RRDtools \n Detección de umbrales",

        f"DEF:{MODULES_NAME[1]}={path_rrd}:{MODULES_NAME[1]}:AVERAGE",

        f"VDEF:cargaMAX={MODULES_NAME[1]},MAXIMUM",
        f"VDEF:cargaMIN={MODULES_NAME[1]},MINIMUM",
        f"VDEF:cargaSTDEV={MODULES_NAME[1]},STDEV",
        f"VDEF:cargaLAST={MODULES_NAME[1]},LAST",
        
        #Umbrales
        # Umbral 20%
        f"CDEF:umbral20={MODULES_NAME[1]},20,LT,0,{MODULES_NAME[1]},IF",
        f"AREA:{MODULES_NAME[1]}#00FFFF:Carga de la RAM", # aqua
        f"AREA:umbral20#7FFFD4:Carga RAM mayor que 20%", # aquamarine
        f"HRULE:15#0000FF:Umbral 20%", # Azul
        # Umbral 50%
        f"CDEF:umbral50={MODULES_NAME[1]},50,LT,0,{MODULES_NAME[1]},IF",
        f"AREA:{MODULES_NAME[1]}#ADFF2F:Carga de la RAM", # greenyellow
        f"AREA:umbral50#9ACD32:Carga RAM mayor que 50%", # yellowgreen
        f"HRULE:15#00FF00:Umbral 50%", # Verde
        # Umbral 90%
        f"CDEF:umbral90={MODULES_NAME[1]},15099494,LT,0,{MODULES_NAME[1]},IF",
        f"AREA:{MODULES_NAME[1]}#FFA500:Carga de la RAM", # orange
        f"AREA:umbral90#FF4500:Carga RAM mayor que 90%", # orangered
        f"HRULE:15#FF0000:Umbral 90%", # Rojo

        "PRINT:cargaLAST:%6.2lf",
        "GPRINT:cargaMIN:%6.2lf %SMIN",
        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
        "GPRINT:cargaLAST:%6.2lf %SLAST"
    )
    carga_stg_img = rrdtool.graphv(
        path_ram,
        "--start", str(tiempo_inicial),
        "--end", str(tiempo_final),
        "--vertical-label=RAM Load",
        '--lower-limit', '0',
        '--upper-limit', ' 16777216',
        "--title=Carga de la RAM del agente Usando SNMP y RRDtools \n Detección de umbrales",

        f"DEF:{MODULES_NAME[1]}={path_rrd}:{MODULES_NAME[1]}:AVERAGE",

        f"VDEF:cargaMAX={MODULES_NAME[1]},MAXIMUM",
        f"VDEF:cargaMIN={MODULES_NAME[1]},MINIMUM",
        f"VDEF:cargaSTDEV={MODULES_NAME[1]},STDEV",
        f"VDEF:cargaLAST={MODULES_NAME[1]},LAST",
        
        #Umbrales
        # Umbral 20%
        f"CDEF:umbral20={MODULES_NAME[1]},20,LT,0,{MODULES_NAME[1]},IF",
        f"AREA:{MODULES_NAME[1]}#00FFFF:Carga de la RAM", # aqua
        f"AREA:umbral20#7FFFD4:Carga RAM mayor que 20%", # aquamarine
        f"HRULE:15#0000FF:Umbral 20%", # Azul
        # Umbral 50%
        f"CDEF:umbral50={MODULES_NAME[1]},50,LT,0,{MODULES_NAME[1]},IF",
        f"AREA:{MODULES_NAME[1]}#ADFF2F:Carga de la RAM", # greenyellow
        f"AREA:umbral50#9ACD32:Carga RAM mayor que 50%", # yellowgreen
        f"HRULE:15#00FF00:Umbral 50%", # Verde
        # Umbral 90%
        f"CDEF:umbral90={MODULES_NAME[1]},90,LT,0,{MODULES_NAME[1]},IF",
        f"AREA:{MODULES_NAME[1]}#FFA500:Carga de la RAM", # orange
        f"AREA:umbral90#FF4500:Carga RAM mayor que 90%", # orangered
        f"HRULE:15#FF0000:Umbral 90%", # Rojo

        "PRINT:cargaLAST:%6.2lf",
        "GPRINT:cargaMIN:%6.2lf %SMIN",
        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
        "GPRINT:cargaLAST:%6.2lf %SLAST"
    )
    
    ultimo_valor_cpu = float(carga_cpu_img["print[0]"])
    ultimo_valor_ram = float(carga_ram_img["print[0]"])
    ultimo_valor_stg = float(carga_stg_img["print[0]"])

    if ( ultimo_valor_cpu > 50 ) and ( ultimo_valor_ram > 50 ):
        pass


