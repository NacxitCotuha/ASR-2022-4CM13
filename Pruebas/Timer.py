import threading
import time
import os

def retrasado():
    nom_hilo = threading.current_thread().getName()
    contador = 1
    while contador <=10:
        print(nom_hilo, 'ejecuta su trabajo', contador)
        time.sleep(0.1)
        contador+=1
    print(nom_hilo, 'ha terminado su trabajo')

hilo1 = threading.Timer(0.2, retrasado)
hilo1.setName('hilo1')
hilo2 = threading.Timer(0.5, retrasado)
hilo2.setName('hilo2')

hilo1.start()
hilo2.start()
print('hilo1 espera 0.2 segundos')
print('hilo2 espera 0.5 segundos')

time.sleep(0.3)
print('hilo2 va a ser cancelado')
hilo2.cancel()
print('hilo2 fue cancelado antes de iniciar su ejecución')


def curlLoop(host: str):
    while True:
        os.system(f"curl {host}") # host, pasar el parametro localhost:3000 como cadena
        time.sleep(5)