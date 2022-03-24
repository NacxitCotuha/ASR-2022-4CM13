# Librerias Python
import sys
import os
import time
import FuncionesRRD


def main() -> None:
    print("Practica 2".center(100, "="))
    try:
        if ( len(sys.argv) == 3 ):
            host_ip: str = sys.argv[0]
            puerto: int = int(sys.argv[1])
            comunidad: str = sys.argv[2]
            if " " in host_ip:
                errorMessage()
            if " " in comunidad:
                errorMessage()
            menu(host_ip=ip, puerto=puerto)
            sys.exit(0)
        else:
            errorMessage()
    except:
        errorMessage()


def menu( host_ip: str, puerto: int ) -> None:
    while verificarConexion():
        print("1. Imprimir Reporte Radius")
        print("2. Crear Reporte txt - Radius")
        print("0.- Salir")
        try:
            opcion = int(input("Seleccionar opcion: "))
            if opcion == 1:
                pass
            elif opcion == 2:
                pass
            elif opcion == 0:
                print("Saliendo del programa...")
                break
        except:
            print("Opcion no valida")


def verificarConexion( host_ip: str, puerto: int, comunidad: str) -> bool:
    contador: int = 0
    estado: bool
    while contador < 5:
        is_up = FuncionesRRD.consultaSNMP(comunidad=comunidad, host=host_ip, oid="1.3.6.1.2.1.1.3.0")
        if is_up:
            estado = True
            break
        estado = False
        contador = contador + 1
        time.sleep(5)
    else:
        if contador >= 5:
            estado = False
        else:
            estado = True
    clearConsole()
    return estado


def clearConsole() -> None:
    command = "clear"
    # if Machine is running on Windows, use cls
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def errorMessage() -> None:
    print("La practica se debe compilar de la siguiente manera: ")
    print("$ python3 main.py <ip:http_service> <port:numero_int> <comunidad:nombre>")
    print("La ip y la comunidad deben ser escritas sin espacios entre si")
    sys.exit(-1)


if __name__ == "__main__":
    main()