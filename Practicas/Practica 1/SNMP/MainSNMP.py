# Funciones de la practica
import DeviceCRUD
import FuncionesRRD
import ReportePDF
# Librerias Python
import sys
import os
from datetime import datetime

def clear_console() -> None:
    command = "clear"
    # if Machine is running on Windows, use cls
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)
    return


def consultar_num_agentes() -> bool:
    rows = DeviceCRUD.leer_bd()
    try:
        no_agentes = 0
        for row in rows:
            no_agentes = no_agentes + 1
        print(f"Numero de agentes registrados: {no_agentes}")
        if no_agentes == 0:
            return False
        else:
            return True
    except:
        print(f"Numero de agentes registrados: No hay Agentes")
        return False


def interfaces_resumen(comunidad: str, host: str, version: int, inter: int) -> None:
    print(f"Resumen de la INTERFACE {inter}".center(50, "-"))
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.1.{inter}", version=version)
    print(f"--> ifIndex(1): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.2.{inter}", version=version)
    print(f"--> ifDescr(2): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.3.{inter}", version=version)
    print(f"--> ifType(3): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.4.{inter}", version=version)
    print(f"--> igMtu(4): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.5.{inter}", version=version)
    print(f"--> ifSpeed(5): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.6.{inter}", version=version)
    print(f"--> ifPhyAddress(6): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.7.{inter}", version=version)
    print(f"--> ifAdminStatus(7): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.8.{inter}", version=version)
    print(f"--> ifOperStatus(8): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.9.{inter}", version=version)
    print(f"--> ifLastChange(9): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.10.{inter}", version=version)
    print(f"--> ifInOctets(10): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.11.{inter}", version=version)
    print(f"--> ifInUcastPkts(11): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.12.{inter}", version=version)
    print(f"--> ifInNUcastPkts(12): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.13.{inter}", version=version)
    print(f"--> ifInDiscards(13): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.14.{inter}", version=version)
    print(f"--> ifInErrors(14): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.15.{inter}", version=version)
    print(f"--> ifInUnknownProtos(15): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.16.{inter}", version=version)
    print(f"--> ifOutOctets(16): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.17.{inter}", version=version)
    print(f"--> ifOutUcastPkts(17): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.18.{inter}", version=version)
    print(f"--> ifOutNUcastPkts(18): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.19.{inter}", version=version)
    print(f"--> ifOutDiscards(19): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.20.{inter}", version=version)
    print(f"--> ifOutErrors(20): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.21.{inter}", version=version)
    print(f"--> ifOutQLen(21): {consulta}")
    consulta = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.22.{inter}", version=version)
    print(f"--> ifSpecific(22): {consulta}")
    return


def resumen_device(comunidad: str, host: str, version: str) -> None:
    # "1.3.6.1.2.1.*"
    print("Iniciando Resumen:")
    ver = 0 if (version == DeviceCRUD.VERSION[1]) else 1
    is_up = FuncionesRRD.consulta_snmp(
        comunidad=comunidad,
        host=host,
        oid="1.3.6.1.2.1.1.3.0", 
        version=ver
    )
    if is_up:
        print("-> Estado: up")
        # Numero de interfaces
        no_interfaces = FuncionesRRD.consulta_snmp(
            comunidad=comunidad,
            host=host,
            oid="1.3.6.1.2.1.2.1.0",
            version=ver
        )
        system = FuncionesRRD.consulta_snmp(
            comunidad=comunidad,
            host=host,
            oid="1.3.6.1.2.1.1.1.0",
            version=ver
        )
        print(f"-> Interfaces: {no_interfaces}")
        interfaces = int(no_interfaces)
        if system:
            print("-> OS: Linux") if ("Linux" in system) else print("-> OS: Windows")
            for interface in range(interfaces):
                interfaces_resumen(comunidad=comunidad, host=host, version=ver, inter=interface + 1)       
        else:
            print("No se lee el if")
        
        for interface in range(interfaces):
            estado_interface7 = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.8.{interface + 1}", version=ver)
            estado_interface8 = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.8.{interface + 1}", version=ver)
            name_interface = FuncionesRRD.consulta_snmp(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.2.2.1.2.{interface + 1}", version=ver)
            print(name_interface)
            if (int(estado_interface7) == 1) and (int(estado_interface8) == 1) and (not (name_interface == "lo")) and ("Linux" in system):
                print(f"->Interfaz a usar: {name_interface}")
                use_interface = interface + 1
                break
            elif (int(estado_interface7) == 1) and (int(estado_interface8) == 1) and ("Intel" in name_interface):
                print(f"->Interfaz a usar: {name_interface}")
                use_interface = interface + 1
                break
        try:
            FuncionesRRD.generar_all_rrd(comunidad=comunidad, host=host, version=ver, interface=use_interface)
        except:
            print("Algo salio mal")
    else:
        print("-> Estado: down")
    print("\n")
    return


# Inicia todos los dispositivos de la BD
def resumen_all_dispositivos() -> None:
    print("Agentes registrados:")
    DeviceCRUD.print_tabla()
    filas = DeviceCRUD.leer_bd()
    for fila in filas:
        id_dis, host, version, comunidad = fila
        print(f"AGENTE: [ID: {id_dis} | COMUNIDAD: {comunidad} | HOST: {host} | VER: {version}]")
        resumen_device(
            comunidad=comunidad,
            host=host,
            version=version
        )


def ingresar_host() -> str:
    host: str
    while True:
        try:
            host = input("Ingrese HOST/IP: ")
            if host == "localhost":
                break
            elif len(host.split(".", maxsplit=10)) == 4:
                ip_str = host.split(".", maxsplit=10)
                is_valid_ip: bool
                for ip_data in ip_str:
                    ip = int(ip_data)
                    is_valid_ip = True if (0 <= ip <= 255) else False
                    if not is_valid_ip:
                        break
                if is_valid_ip:
                    break
                else:
                    print(f"El host [{host}] no es valido intentelo de nuevo")
                    continue
            else:
                print(f"El host [{host}] no es valido intentelo de nuevo")
                continue
        except:
            print(f"El host [{host}] no es valido intentelo de nuevo")
            continue
    return host.strip()


def ingresar_ver() -> int:
    ver: int
    while True:
        try:
            ver = int(input("Ingrese la version SNMP (1 o 2): "))
            if (ver == 1) or (ver == 2):
                break
            else:
                print(f"La version [{ver}] no es valida, intentelo nuevamente")
                continue
        except:
            print("Dato no valido intentelo nuevamente")
            continue
    return ver


def ingresar_comunidad() -> str:
    comunidad: str
    while True:
        comunidad = input("Ingrese comunidad: ")
        if comunidad == " ":
            print("Comunidad no valida, intentelo de nuevo")
            continue
        elif "." in comunidad:
            print("Comunidad no valida, intentelo de nuevo")
            continue
        else:
            break
    return comunidad.strip()


def agregar_agente() -> None:
    clear_console()
    print("Agregar Nuevo Agente".center(50, " "))
    host = ingresar_host()
    ver = ingresar_ver()
    comunidad = ingresar_comunidad()
    DeviceCRUD.agregar_bd(
        host=host,
        ver=DeviceCRUD.VERSION[ver],
        comunidad=comunidad
    )
    resumen_device(
        comunidad=comunidad,
        host=host,
        version=DeviceCRUD.VERSION[ver],
    )
    return


def actualizar_agente() -> None:
    clear_console()
    DeviceCRUD.print_tabla()
    while True:
        print("Actualizar Dispositivo".center(50, " "))
        print("1. Actualizar HOST")
        print("2. Actualizar VERSION")
        print("3. Actualizar COMUNIDAD")
        print("4. Salir de actualizaciones")
        try:
            opcion = int(input("Seleccione la opcion: "))
            if opcion == 1:
                host = ingresar_host()
                try:
                    id_dis = int(input("Inserte el ID del Dispositivo: "))
                    DeviceCRUD.actualizar_host_bd(id_dis=id_dis, host=host)
                    DeviceCRUD.print_tabla()
                    break
                except:
                    print("El ID es incorrecto intentelo de nuevo")
                    continue
            elif opcion == 2:
                version = ingresar_ver()
                try:
                    id_dis = int(input("Inserte el ID del Dispositivo: "))
                    DeviceCRUD.actualizar_ver_bd(id_dis=id_dis, ver=DeviceCRUD.VERSION[version])
                    DeviceCRUD.print_tabla()
                    break
                except:
                    print("El ID es incorrecto intentelo de nuevo")
                    continue
            elif opcion == 3:
                comunidad = ingresar_comunidad()
                try:
                    id_dis = int(input("Inserte el ID del Dispositivo: "))
                    DeviceCRUD.actualizar_comunidad_bd(id_dis=id_dis, comunidad=comunidad)
                    DeviceCRUD.print_tabla()
                    break
                except:
                    print("El ID es incorrecto intentelo de nuevo")
                    continue
            elif opcion == 4:
                print("Saliendo de Actualizar Dispositivos...")
                break
            else:
                print("Opcion no valida, intentelo de nuevo")
        except:
            print("Dato no valido intentelo de nuevo")
            continue
    return


def eliminar_agente() -> None:
    clear_console()
    DeviceCRUD.print_tabla()
    while True:
        print("Seccion de eliminar Dispositivo".center(50, " "))
        opcion = input("Ingrese el ID del dispositivo a eliminar o 'N' si quiere salir: ")
        if opcion == "N":
            break
        else:
            try:
                id_dis = int(opcion)
                DeviceCRUD.eliminar_bd(id_dis=id_dis)
                break
            except:
                print("Opcion no valida, intentelo de nuevo")
                continue
    DeviceCRUD.print_tabla()
    return


def generar_reportes_pdf():
    clear_console()
    print("Generador de Reportes de Agentes(Activos: UP)".center(50, " "))
    DeviceCRUD.print_tabla
    filas = DeviceCRUD.leer_bd()
    fecha = datetime.today().strftime("%Y-%m-%d")
    for fila in filas:
        id_dis, host, version, comunidad = fila
        ver = 0 if (version == DeviceCRUD.VERSION[1]) else 1
        system = FuncionesRRD.consulta_snmp(
            comunidad=comunidad,
            host=host,
            oid="1.3.6.1.2.1.1.1.0",
            version=ver
        )
        if system:
            print(f"{id_dis} | {host} | {comunidad} | {version} | ACTIVO")
            ReportePDF.crear_pdf(host=host, comunidad=comunidad, ver=ver, system=system, fecha=fecha)
        else:
            print(f"El agente [{id_dis},{host},{version},{comunidad}] no esta actualmente activo")
    return


def menu_agentes() -> None:
    while True:
        # Opciones
        print("Menu Agentes".center(50, " "))
        print("1. Agregar Agente")
        print("2. Actualizar Agente")
        print("3. Eliminar Agente")
        print("4. Generar Reportes PDF")
        print("5. Salir")
        try:
            opcion = int(input("Selecciona tu opcion: "))
            if opcion == 1:
                agregar_agente()
            elif opcion == 2:
                actualizar_agente()
            elif opcion == 3:
                eliminar_agente()
            elif opcion == 4:
                generar_reportes_pdf()
            elif opcion == 5:
                print("Saliendo del programa...")
                break
            else:
                print(f"Opcion {opcion} no existe")
            continue
        except:
            print("Tu opcion no es valida")
            continue



if __name__ == "__main__":
    print("Practica 1: Adquisición de información usando SNMP".center(100, "="))
    DeviceCRUD.verificar_bd()
    if consultar_num_agentes():
        resumen_all_dispositivos()
    menu_agentes()
    sys.exit()
