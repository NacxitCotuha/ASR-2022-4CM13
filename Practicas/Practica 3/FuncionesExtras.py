# Constante
DIRECTORY_RRD = "RRD" # Carpeta para archivos RRD
DIRECTORY_XML = "XML" # Carpeta para archivos XML
DIRECTORY_IMG = "IMG" # Carpeta para archivos IMG
MODULES_NAME = (
    "cargaCPU",
    "cargaRAM",
    "cargaSTG",
)

def hexToString( cadena ) -> str:
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