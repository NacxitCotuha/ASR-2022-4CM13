# Librerias Python
import sys
import os
import threading
import time
# Archivos Practica
import CrudRRD
import ReporteRadius

def main() -> None:
    print("Practica 2".center(100, "="))
    if len(sys.argv) != 3:
        errorMessage(sys.argv[0])
    try:
        host_ip: str = sys.argv[1]
        if not verificarHostIP(host_ip=host_ip):
            errorMessage(sys.argv[0])
        comunidad: str = sys.argv[2]
        menu(host_ip=host_ip, comunidad=comunidad)
        sys.exit(0)
    except ValueError:
        errorMessage(sys.argv[0])


def menu( host_ip: str, comunidad: str ) -> None:
    while verificarConexion(host_ip=host_ip, comunidad=comunidad):
        crearDemonio(host_ip=host_ip, comunidad=comunidad)
        print("1. Imprimir Reporte Radius")
        print("2. FetchRRD")
        print("0.- Salir")
        try:
            opcion = int(input("Seleccionar opcion: "))
            if opcion == 1:
                clearConsole()
                ReporteRadius.imprimirReporte(host=host_ip, comunidad=comunidad)
            elif opcion == 2:
                clearConsole()
                path_rrd = CrudRRD.crearPathRRD(host=host_ip, comunidad=comunidad)
                CrudRRD.fetchRRD(path_rrd=path_rrd)
            elif opcion == 0:
                print("Saliendo del programa...")
                break
        except ValueError:
            print("Opcion no valida")
    else:
        print(f"Error de conexion: No se pudo establecer conexión con {host_ip}: {comunidad}")


def verificarHostIP( host_ip: str) -> bool:
    if "localhost" == host_ip:
        return True
    else:
        try:
            ip_separada = host_ip.split(sep=".", maxsplit=6)
            if len(ip_separada) != 4:
                return False
            else:
                is_validIP: bool = False
                for ip_dato in ip_separada:
                    ip_num = int(ip_dato)
                    is_validIP = True if ( 0 <= ip_num <= 255 ) else False
                    if not is_validIP:
                        break
                return is_validIP
        except ValueError:
            errorMessage(sys.argv[0])


def verificarConexion( host_ip: str, comunidad: str ) -> bool:
    print(f"Iniciando conexion con {comunidad} en {host_ip}...")
    contador: int = 0
    estado: bool = False
    while contador < 5:
        print(f"Intento de conexion {contador + 1}...")
        is_up = CrudRRD.consultaSNMP(comunidad=comunidad, host=host_ip, oid="1.3.6.1.2.1.1.3.0")
        if is_up:
            estado = True
            break
        estado = False
        contador = contador + 1
        time.sleep(5)
    return estado


def crearDemonio( host_ip: str, comunidad: str ) -> None:
    print(f"Creando demonio para IP: {host_ip}, comunidad: {comunidad}")
    path_rrd = CrudRRD.crearPathRRD(host=host_ip, comunidad=comunidad)
    if not os.path.isfile(path=path_rrd):
        CrudRRD.crearRRD(path=path_rrd)
    demonio_update = threading.Thread(
        target=CrudRRD.updateRRDHTTP,
        args=(path_rrd, comunidad, host_ip),
        daemon=True
    )
    demonio_update.start()




def clearConsole() -> None:
    command = "clear"
    # if Machine is running on Windows, use cls
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def errorMessage( program_name: str ) -> None:
    print("La practica se debe compilar de la siguiente manera: ")
    print(f"$ python3 {program_name} <ip:http_service> <comunidad:nombre>")
    print("La ip y la comunidad deben ser escritas sin espacios entre si")
    sys.exit(-1)


if __name__ == "__main__":
    main()