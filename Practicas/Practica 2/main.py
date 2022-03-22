# Librerias Python
import sys


def main() -> None:
    print("Practica 2".center(100, "="))
    try:
        if ( len(sys.argv) == 2 ):
            ip: str = sys.argv[0]
            puerto: int = int(sys.argv[1])
            sys.exit(0)
        else:
            errorMessage()
    except:
        errorMessage()





def errorMessage() -> None:
    print("La practica se debe compilar de la siguiente manera: ")
    print("$ python3 main.py <ip:http_service> <port:numero_int>")
    sys.exit(-1)


if __name__ == "__main__":
    main()