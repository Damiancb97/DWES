from operaciones import suma, resta, multiplicacion, division

def solicitar_numero(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Por favor, introduce un número válido.")

def main():
    print("Bienvenido a la calculadora")

    while True:
        num1 = solicitar_numero("Introduce el primer número: ")
        num2 = solicitar_numero("Introduce el segundo número: ")

        print("\nSelecciona una operación:")
        print("1 - Suma")
        print("2 - Resta")
        print("3 - Multiplicación")
        print("4 - División")

        opcion = input("Elige una opción (1/2/3/4): ")

        if opcion == '1':
            resultado = suma(num1, num2)
            print(f"Resultado de la suma: {resultado}")
        elif opcion == '2':
            resultado = resta(num1, num2)
            print(f"Resultado de la resta: {resultado}")
        elif opcion == '3':
            resultado = multiplicacion(num1, num2)
            print(f"Resultado de la multiplicación: {resultado}")
        elif opcion == '4':
            resultado = division(num1, num2)
            print(f"Resultado de la división: {resultado}")
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            continue

        repetir = input("\n¿Quieres hacer otra operación? (s/n): ").strip().lower()
        if repetir != 's':
            print("Gracias por usar la calculadora. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
