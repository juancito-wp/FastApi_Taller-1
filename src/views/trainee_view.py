import re

from src.models import trainee_model
from src.templates import trainee_template

# ==========================================

# INICIALIZACIÓN Y VISTAS EXISTENTES

# ==========================================

def init_app_data():
    """Inicializa los datos de la aplicación."""
    trainee_model.load_trainees()

def register_trainee_view():
    """Lógica para procesar el registro de un aprendiz desde la vista."""

    data = trainee_template.get_trainee_input()

    doc = data.get("documento")

    if trainee_model.search_by_document(doc):
        trainee_template.display_message(
            {
                "type": "error",
                "text": "Ya existe un aprendiz registrado con este número de documento.",
            }
        )
        return

    trainee_model.register_trainee(data)

    nombre = data.get("nombre")
    ficha = data.get("ficha")

    trainee_template.display_message(
        {
            "type": "success",
            "text": f"Aprendiz {nombre} registrado exitosamente en la ficha {ficha}.",
        }
    )


def status_view():
    """Muestra el estado actual de la lista de aprendices registrados."""

    all_trainees = trainee_model.load_trainees()

    trainee_template.display_trainee_list(all_trainees)

# ==========================================

# PUNTO 2: FUNCIONES DE VALIDACIÓN DE ENTRADA

# ==========================================

def validate_text(prompt):
    """Garantiza que el usuario ingrese solo letras y espacios."""

    while True:
        text = input(prompt).strip()

    if text and text.replace(" ", "").isalpha():
        return text.title()

    print("❎ Error: solo se permiten letras y espacios. Intente nuevamente.")


def validate_number(prompt):
    """Garantiza que el usuario ingrese solo números."""

    while True:
        number = input(prompt).strip()

    if number.isdigit():
        return number

    print("❎ Error: solo se permiten números. Intente nuevamente.")


def validate_email(prompt):
    """Garantiza un formato de correo electrónico válido."""


    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    while True:
        email = input(prompt).strip().lower()

    if re.match(pattern, email):
        return email

    print("❎ Error: formato de correo electrónico inválido. Intente nuevamente.")


# ==========================================

# PUNTO 3: EDITAR APRENDIZ

# ==========================================

def edit_trainee_view():
    """Captura el documento y los nuevos datos para editar un aprendiz."""

    print("\n--- EDITAR APRENDIZ ---")

    document = validate_number(
    "Ingrese el número de documento del aprendiz a editar: "
    )

    if not trainee_model.search_by_document(document):
        trainee_template.display_message(
        {
            "type": "error",
            "text": "No se encontró ningún aprendiz registrado con ese documento.",
        }
    )
    return

    print("\nIngrese los nuevos datos del aprendiz:")

    new_name = validate_text("Nuevo nombre completo: ")
    new_group = validate_number("Nueva ficha: ")
    new_email = validate_email("Nuevo correo electrónico: ")
    new_program = validate_text("Nuevo programa de formación: ")

    updated_data = {
    "nombre": new_name,
    "ficha": new_group,
    "email": new_email,
    "programa": new_program,
    }

    if trainee_model.update_trainee(document, updated_data):
        trainee_template.display_message(
        {
            "type": "success",
            "text": "Aprendiz actualizado exitosamente.",
        }
    )
    else:
        trainee_template.display_message(
        {
            "type": "error",
            "text": "No se pudo actualizar el aprendiz.",
        }
    )


# ==========================================

# PUNTO 4: ELIMINAR APRENDIZ

# ==========================================

def delete_trainee_view():
    """Captura el documento y solicita la eliminación del aprendiz."""

    print("\n--- ELIMINAR APRENDIZ ---")

    document = validate_number(
    "Ingrese el número de documento del aprendiz a eliminar: "
    )

    if trainee_model.delete_trainee(document):
        trainee_template.display_message(
            {
                "type": "success",
                "text": "Aprendiz eliminado exitosamente.",
            }
        )
    else:
        trainee_template.display_message(
        {
            "type": "error",
            "text": "No se encontró ningún aprendiz registrado con ese documento.",
        }
    )


# ==========================================

# PUNTO 5: BUSCAR APRENDIZ

# ==========================================

def search_trainees_view():
    """Busca aprendices por nombre o número de ficha."""


    print("\n--- BUSCAR APRENDIZ ---")

    term = input(
    "Ingrese el nombre o el número de ficha a buscar: "
    ).strip()

    if not term:
        trainee_template.display_message(
        {
            "type": "error",
            "text": "Debe ingresar un término de búsqueda válido.",
        }
    )
    return

    results = trainee_model.search_trainees_by_term(term)

    if results:
        trainee_template.display_trainee_list(results)
    else:
        trainee_template.display_message(
        {
            "type": "error",
            "text": f"No se encontraron aprendices con la coincidencia '{term}'.",
        }
    )


# ==========================================

# PUNTO 6: EXPORTAR A CSV

# ==========================================

def export_trainees_view():
    """Solicita la exportación de aprendices a un archivo CSV."""
    print("\n--- EXPORTAR APRENDICES A CSV ---")

    success, result = trainee_model.export_trainees_to_csv()

    if success:
        trainee_template.display_message(
        {
            "type": "success",
            "text": f"Datos exportados exitosamente al archivo: {result}",
        }
    )
    else:
        trainee_template.display_message(
        {
            "type": "error",
            "text": f"Error al exportar: {result}",
        }
    )


# ==========================================

# PUNTO 7: MENÚ PRINCIPAL

# ==========================================

def main_menu_controller():
    """Muestra el menú principal de la aplicación."""

    while True:
        print("\n========== SISTEMA DE APRENDICES ==========")
        print("1. Registrar aprendiz")
        print("2. Ver aprendices")
        print("3. Editar aprendiz")
        print("4. Eliminar aprendiz")
        print("5. Buscar aprendiz")
        print("6. Exportar a CSV")
        print("7. Salir")

        option = input("\nSeleccione una opción: ").strip()

        if option == "1":
            register_trainee_view()

        elif option == "2":
            status_view()

        elif option == "3":
            edit_trainee_view()

        elif option == "4":
            delete_trainee_view()

        elif option == "5":
            search_trainees_view()

        elif option == "6":
            export_trainees_view()

        elif option == "7":
            print("\n👋 Saliendo del programa...")
            break

        else:
            print("\n❌ Opción inválida. Intente nuevamente.")
