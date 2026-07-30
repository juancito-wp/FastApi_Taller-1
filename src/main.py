import sys
import os

# Aseguramos que Python reconozca la raíz del proyecto para importar desde 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.views import trainee_view

# ==========================================
# PUNTO 7: MENÚ PRINCIPAL
# ==========================================

def display_main_menu():
    """Muestra las opciones del menú principal en la consola."""
    print("\n" + "=" * 45)
    print("     SISTEMA DE GESTIÓN DE APRENDICES      ")
    print("=" * 45)
    print("1. Registrar nuevo aprendiz")
    print("2. Ver lista de aprendices")
    print("3. Editar datos de aprendiz")
    print("4. Eliminar aprendiz")
    print("5. Buscar aprendiz (por nombre o ficha)")
    print("6. Exportar lista a CSV")
    print("7. Salir")
    print("=" * 45)

def main():
    """Función principal que controla el flujo de la aplicación."""
    # Inicializa el directorio data/ y los datos
    trainee_view.init_app_data()

    while True:
        display_main_menu()
        option = input("Seleccione una opción (1-7): ").strip()

        if option == "1":
            trainee_view.register_trainee_view()
        elif option == "2":
            trainee_view.status_view()
        elif option == "3":
            trainee_view.edit_trainee_view()
        elif option == "4":
            trainee_view.delete_trainee_view()
        elif option == "5":
            trainee_view.search_trainees_view()
        elif option == "6":
            trainee_view.export_trainees_view()
        elif option == "7":
            print("\n👋 ¡Gracias por usar el sistema! Saliendo del programa...")
            break
        else:
            print("❌ Opción inválida. Por favor, seleccione un número del 1 al 7.")

if __name__ == "__main__":
    main()

"""
Actividades a realizar:
1. Refactorizar ruta del archivo JSON en la carpeta data/
2. Refactorizar validaciones de los datos de entrada(incluir el correo electrónico) en la vista para que sean más robustas y claras.(Númerica, alfabética, correo electrónico, etc.)
3. Implementar el editar de aprendices para permitir modificar los datos de un aprendiz existente.
4. Implementar la eliminación de aprendices para permitir borrar un aprendiz existente de la lista.
5. Implementar la búsqueda de aprendices por nombre o ficha para facilitar la localización de registros específicos.
6. Implementar la exportación de la lista de aprendices a un archivo CSV para facilitar el manejo de datos fuera del programa.
7. Implementar un menú principal para que el usuario pueda elegir entre registrar, editar, eliminar, buscar o exportar aprendices, en lugar de solo registrar uno tras otro."""