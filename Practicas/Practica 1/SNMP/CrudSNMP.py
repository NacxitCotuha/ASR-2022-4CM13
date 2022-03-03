import os
import sqlite3


NAME_BD = "DataSNMP.db"


version: dict[int, str] = {
    1: "Version_1",
    2: "Version_2"
}


def verificar_bd() -> None:
    if os.path.isfile(NAME_BD):
        print("La BD de los dispositivos existe leyendo informacion...")
        read_bd()
    else:
        print("La BD de los dispositivos no existe, creando la BD...")
        create_bd()
    return


def connect_bd() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(NAME_BD)
        return conn
    except sqlite3.Error:
        print(sqlite3.Error)


def create_bd() -> None:
    conn = connect_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute("CREATE TABLE dispositivos(id INTEGER PRIMARY KEY, host TEXT NOT NULL, version TEXT NOT NULL, comunidad TEXT NOT NULL, port INTEGER NOT NULL)")
    conn.commit()
    conn.close()


def insert_bd(host: str, version: str, comunidad: str, puerto: int) -> None:
    entities = (host, version, comunidad, puerto)
    conn = connect_bd()
    cursor_obj = conn.cursor()
    try:
        cursor_obj.execute("INSERT INTO dispositivos(host, version, comunidad, port) VALUES (?, ?, ?, ?)", entities)
        print(f"Se añadio de forma correcta los siguientes datos: {entities}")
        conn.commit()
    except sqlite3.DatabaseError:
        cursor_obj.execute("CREATE TABLE dispositivos(id INTEGER PRIMARY KEY, host TEXT NOT NULL, version TEXT NOT NULL, comunidad TEXT NOT NULL, port INTEGER NOT NULL)")
        conn.commit()
        cursor_obj.execute("INSERT INTO dispositivos(host, version, comunidad, port) VALUES (?, ?, ?, ?)", entities)
        print(f"Se añadio de forma correcta los siguientes datos: {entities}")
        conn.commit()
    conn.close()


def read_bd() -> any:
    conn = connect_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute("SELECT * from dispositivos")
    rows = cursor_obj.fetchall()

    for row in rows:
        yield row


# Actualizar HOST o IP
def update_host_bd(id_dis: int, host: str) -> None:
    conn = connect_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute(f"UPDATE dispositivos SET host = \"{host}\" WHERE id = {id_dis}")
    conn.commit()
    conn.close()
    return


# Actualizar Version del SNMP
def update_version_bd(id_dis: int, version: str) -> None:
    conn = connect_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute(f"UPDATE dispositivos SET version = \"{version}\" WHERE id = {id_dis}")
    conn.commit()
    conn.close()
    return


# Actualizar Nombre de la Comunidad
def update_comunidad_bd(id_dis: int, comunidad: str) -> None:
    conn = connect_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute(f"UPDATE dispositivos SET comunidad = \"{comunidad}\" WHERE id = {id_dis}")
    conn.commit()
    conn.close()
    return


# Actualizar Puerto
def update_puerto_bd(id_dis: int, puerto: str) -> None:
    conn = connect_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute(f"UPDATE dispositivos SET port = {puerto} WHERE id = {id_dis}")
    conn.commit()
    conn.close()
    return


# Eliminar un Dispositivo
def delete_bd(id_dis: int) -> None:
    try:
        conn = connect_bd()
        cursor_obj = conn.cursor()
        cursor_obj.execute(f"DELETE FROM dispositivos WHERE id = {id_dis}")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError:
        print("El Archivo a Eliminar no existe") 
    return


def print_tabla() -> None:
    filas = read_bd()
    print("[{0}]    [{1:15s}]    [{2:10s}]    [{3:20s}]    [{4:5s}]".format(
            "ID", "HOST", "SNMP Ver.", "Name Comunity", "Port"))
    for fila in filas:
        id_dis, host, version, comunidad, puerto = fila;
        print("{0:4}    {1:17s}    {2:12s}    {3:20s}    {4:7}".format(id_dis, host, version, comunidad, puerto))
    return


if __name__ == "__main__":
    verificar_bd()
    insert_bd("localhost", version[2], "comunidadSNMP", 50000)
    print_tabla()
    update_comunidad_bd(2, comunidad="ComunidadDelAnillo")
    update_host_bd(3, host="192.168.0.2")
    update_puerto_bd(4, puerto=8080)
    update_version_bd(1, version=version[2])
    print_tabla()
    delete_bd(5)
    print_tabla()