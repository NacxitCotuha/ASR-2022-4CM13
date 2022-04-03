import sys
import time

import requests

def main() -> None:
    print("Iniciando trafico del servicio HTTP...")
    if len(sys.argv) != 2:
        errorMessage()
    host_ip = sys.argv[1]
    if verificarIP( host_ip=host_ip ):
        url_http = f"http://{host_ip}:3000"
        while True:
            respuesta = requests.get(url_http)
            print(respuesta)
            time.sleep(2)


def verificarIP( host_ip:str ) -> bool:
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
            errorMessage()

def errorMessage() -> None:
    program_name = sys.argv[0]
    print("La practica se debe compilar de la siguiente manera: ")
    print(f"$ python3 {program_name} <ip:http_service>")
    print("La ip deben ser escrito sin espacios entre si")
    sys.exit(-1)


if __name__ == "__main__":
    main()