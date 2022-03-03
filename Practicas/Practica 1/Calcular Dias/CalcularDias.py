from datetime import datetime

def seleccionar_modulo(total_dias: int) -> None:
    print(f"Sacando el resultado de total de dias % 3 las posibles opciones son: ")
    print(f"\tR = 0 -> Modulo 1")
    print(f"\tR = 1 -> Modulo 2")
    print(f"\tR = 2 -> Modulo 3")
    print(f"Se calculara la opcion que te toca...")
    
    print(f"Resultado: ")
    if total_dias % 3 == 0:
        print(f"{total_dias} % 3 = 0 te toco el Modulo 1")
    elif total_dias % 3 == 1:
        print(f"{total_dias} % 3 = 1 te toco el Modulo 2")
    elif total_dias % 3 == 2:
        print(f"{total_dias} % 3 = 2 te toco el Modulo 3")
    else:
        print(f'{total_dias} % 3 = {total_dias % 3} por lo visto te salvaste de alguna forma :v')


if __name__ == '__main__':
    print("Programa para calcular los dias vividos hasta el 23 de Febrero del 2022")
    fechaFin = datetime(2022, 2, 23) # 23 de Febrero de 2022
    print("Ingrese su fecha de Nacimiento")
    d: int
    m: int
    a: int
    while True:
        try:
            d = int(input("Ingrese dia (int): "))
            m = int(input("Ingrese mes (int): "))
            a = int(input("Ingrese año (int): "))
            break
        except Exception as e:
            print("Error al ingresar la fecha, intentelo otra vez...")
            continue
    fechaInicial = datetime(a, m, d)
    print(f"Fecha Ingresada en formato (YYYY-MM-DD): {fechaInicial}")
    diasTotal = fechaFin - fechaInicial
    print(f"Numero de dias vivido = {diasTotal.days}")
    seleccionar_modulo(total_dias=diasTotal.days)
