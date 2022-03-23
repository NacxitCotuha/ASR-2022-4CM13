# Librerias Python
import sys
import os
import time


def main() -> None:
    print("Practica 2".center(100, "="))
    try:
        if ( len(sys.argv) == 2 ):
            ip: str = sys.argv[0]
            puerto: int = int(sys.argv[1])
            menu(host_ip=ip, puerto=puerto)
            sys.exit(0)
        else:
            errorMessage()
    except:
        errorMessage()


def menu( host_ip: str, puerto: int ) -> None:
    while True:
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


def verificarConexion() -> bool:
    time.sleep(5)


def clearConsole() -> None:
    command = "clear"
    # if Machine is running on Windows, use cls
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def errorMessage() -> None:
    print("La practica se debe compilar de la siguiente manera: ")
    print("$ python3 main.py <ip:http_service> <port:numero_int>")
    sys.exit(-1)


if __name__ == "__main__":
    main()