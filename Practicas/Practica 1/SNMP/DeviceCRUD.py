import os
import sqlite3


NAME_BD = "AgentsSNMP.db"


VERSION: dict[int, str] = {
    1: "Version1",
    2: "Version2"
}


def verificar_bd() -> None:
    if os.path.isfile(NAME_BD):
        print("La BD de los dispositivos existe leyendo informacion...")
        leer_bd()
    else:
        print("La BD de los dispositivos no existe, creando la BD...")
        crear_bd()
    return


def conectar_bd() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(NAME_BD)
        return conn
    except sqlite3.Error:
        print(sqlite3.Error)


def crear_bd() -> None:
    conn = conectar_bd()
    cursor_obj = conn.cursor()
    # No hay puerto por que se define con la version de SNMP
    cursor_obj.execute("CREATE TABLE agentes(id INTEGER PRIMARY KEY, host TEXT NOT NULL, version TEXT NOT NULL, comunidad TEXT NOT NULL)")
    conn.commit()
    conn.close()


def agregar_bd(host: str, ver: str, comunidad: str) -> None:
    entidades = (host, ver, comunidad)
    conn = conectar_bd()
    cursor_obj = conn.cursor()
    try:
        cursor_obj.execute("INSERT INTO agentes(host, version, comunidad) VALUES (?, ?, ?)", entidades)
        conn.commit()
        print(f"Se añadio correctamente el agente: {entidades}")
    except sqlite3.DatabaseError:
        crear_bd()
        cursor_obj.execute("INSERT INTO agentes(host, version, comunidad) VALUES (?, ?, ?)", entidades)
        conn.commit()
        print(f"Se añadio correctamente el agente: {entidades}")
    finally:
        conn.close()
        return


def leer_bd() -> any:
    conn = conectar_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute("SELECT * FROM agentes")
    rows = cursor_obj.fetchall()
    for row in rows:
        yield row


def actualizar_host_bd(id_dis: int, host: str) -> None:
    conn = conectar_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute(f"UPDATE agentes SET host = \"{host}\" WHERE id = {id_dis}")
    conn.commit()
    conn.close()
    return


def actualizar_ver_bd(id_dis: int, ver: str) -> None:
    conn = conectar_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute(f"UPDATE agentes SET version = \"{ver}\" WHERE id = {id_dis}")
    conn.commit()
    conn.close()
    return


def actualizar_comunidad_bd(id_dis: int, comunidad: str) -> None:
    conn = conectar_bd()
    cursor_obj = conn.cursor()
    cursor_obj.execute(f"UPDATE agentes SET comunidad = \"{comunidad}\" WHERE id = {id_dis}")
    conn.commit()
    conn.close()
    return


def eliminar_bd(id_dis: int) -> None:
    try:
        conn = conectar_bd()
        cursor_obj = conn.cursor()
        cursor_obj.execute(f"DELETE FROM agentes WHERE id = {id_dis}")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError:
        print("El Archivo a Eliminar no existe") 
    finally:
        return

def print_tabla() -> bool:
    try:
        filas = leer_bd()
        print("[{0}]    [{1:15s}]    [{2:10s}]    [{3:30s}] ".format(
                "ID", "HOST", "SNMP Ver.", "Name Comunity"))
        for fila in filas:
            id_dis, host, version, comunidad = fila;
            print("{0:4}    {1:17s}    {2:12s}    {3:32s}".format(id_dis, host, version, comunidad))
        return True
    except sqlite3.Error:
        print("La BD esta vacia, no hay agentes")
        return False