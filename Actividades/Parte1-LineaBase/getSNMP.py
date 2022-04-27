from pysnmp.hlapi import *


def consultarSNMP( comunidad: str, host: str, oid: str ):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(
            SnmpEngine(),
            CommunityData(comunidad),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
    )
    if error_indication:
        print(error_indication)
    elif error_status:
        print('%s at %s' % (error_status.prettyPrint(), error_index and var_binds[int(error_index) - 1][0] or '?'))
    else:
        for var_bind in var_binds:
            var_b = (' = '.join([x.prettyPrint() for x in var_bind]))
            resultado = var_b.split()[2]
        return resultado
