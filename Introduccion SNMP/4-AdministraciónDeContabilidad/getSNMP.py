from pprint import pformat
from pysnmp.hlapi import *

def consultarSNMP(comunidad: str, host: str, oid: str):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(
            SnmpEngine(),
            CommunityData(comunidad),
            UdpTransportTarget((host, 161)),
            ContextData(), 
            ObjectType(ObjectIdentity(oid))
        )
    )

    if errorIndication:
        print(errorIndication)
    
    elif errorStatus:
        print(f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
    
    else:
        for varBind in varBinds:
            varB=(" = ".join([x.prettyPrint() for x in varBind]))
            resultado = varB.split()[2]
        return resultado
