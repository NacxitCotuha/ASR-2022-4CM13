from datetime import datetime
import CrudRRD


def imprimirReporte( host: str, comunidad: str ) -> None:
    systemData = CrudRRD.consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.1.1.0")
    systemTime = CrudRRD.consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.1.3.0")
    tcpConnState = CrudRRD.consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.6.13.1.1.0.0.0.0.3000.0.0.0.0.0")
    tcpConnLocalDireccion = CrudRRD.consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.6.13.1.2.0.0.0.0.3000.0.0.0.0.0")
    tcpConnLocalPort = CrudRRD.consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.6.13.1.3.0.0.0.0.3000.0.0.0.0.0")
    tcpConnRemAddress = CrudRRD.consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.6.13.1.4.0.0.0.0.3000.0.0.0.0.0")
    tcpConnRemPort = CrudRRD.consultaSNMP(comunidad=comunidad, host=host, oid=f"1.3.6.1.2.1.6.13.1.5.0.0.0.0.3000.0.0.0.0.0")
    start, end, tcpInSeg, tcpOutSeg = CrudRRD.promedioRRD(host=host, comunidad=comunidad)
    fecha_inicio = datetime.fromtimestamp(start)
    fecha_fin = datetime.fromtimestamp(start)
    os_system = "Linux" if "Linux" in systemData else "Windows"

    print("Reporte Radius".center(50, "-"))
    print(f"device: {os_system}")
    print(f"description: HTTP Server 3000")
    print(f"date: {fecha_inicio}")
    print(f"defaultProtocol: radius\n")

    print(f"rdate: {fecha_fin}")
    print("#Host-IP-Address")
    print(f"0: {host}")
    print("#HTTP-Connection-State")
    print(f"1: {tcpConnState}")
    print("#HTTP-Connection-Local-Direction")
    print(f"2: {tcpConnLocalDireccion}")
    print("#HTTP-Connection-Local-Port")
    print(f"3: {tcpConnLocalPort}")
    print("#HTTP-Connection-Remote-Address")
    print(f"4: {tcpConnRemAddress}")
    print("#HTTP-Connection-Remote-Port")
    print(f"5: {tcpConnRemPort}")
    print("#HTTP-Session-Time")
    print(f"6: {systemTime}")
    print("#HTTP-Input-Segment")
    print(f"10: {tcpInSeg}")
    print("HTTP-Output-Segment")
    print(f"11: {tcpOutSeg}")

    print("Fin Reporte Radius".center(50, "-"))
    print()




