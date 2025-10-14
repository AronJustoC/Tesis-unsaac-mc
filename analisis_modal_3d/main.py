def realizar_analisis_estatico():
    print("Iniciando análisis estático...")
    # Aquí solicitaré los datos y ejecutaré el análisis estático.

def realizar_analisis_modal():
    print("Iniciando análisis modal...")
    # Aquí solicitaré los datos y ejecutaré el análisis modal.

def realizar_analisis_armonico():
    print("Iniciando análisis armónico...")
    # Aquí solicitaré los datos y ejecutaré el análisis armónico.

def main_menu():
    while True:
        print("\n--- MENÚ PRINCIPAL DE ANÁLISIS ESTRUCTURAL ---")
        print("1. Análisis Estático")
        print("2. Análisis Modal")
        print("3. Análisis de Respuesta Armónica")
        print("4. Salir")
        choice = input("Seleccione una opción (1-4): ")

        if choice == '1':
            realizar_analisis_estatico()
        elif choice == '2':
            realizar_analisis_modal()
        elif choice == '3':
            realizar_analisis_armonico()
        elif choice == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main_menu()
