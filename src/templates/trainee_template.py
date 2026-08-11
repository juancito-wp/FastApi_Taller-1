# Capa TEMPLATE: Interfaz de usuario por consola para registrar aprendices

def get_trainee_input():
    """Solicita al usuario los datos para registrar un aprendiz."""


    document_id = input("Número de documento: ").strip()
    type_id = input("Tipo de documento (CC/TI/CE): ").strip().upper()
    name = input("Nombre completo: ").strip().title()
    email = input("Correo electrónico: ").strip().lower()
    group_code = input("Número de Ficha: ").strip()
    program = input("Programa de Formación: ").strip().title()

    return {
    "tipo_doc": type_id,
    "documento": document_id,
    "nombre": name,
    "email": email,
    "ficha": group_code,
    "programa": program,
    }


def display_message(message):
    icons = {
    "success": "✅ ",
    "error": "⚠️ ",
    "info": "ℹ️ ",
    }


    print(f"{icons.get(message['type'], '')}{message['text']}")


def display_trainee_list(trainees):
    """Muestra la lista de aprendices registrados."""


    if not trainees:
        print("No hay aprendices registrados.")
    else:
        print("\n--- Lista de Aprendices Registrados ---")

    for trainee in trainees:
        print(
        f"Documento: {trainee.get('documento', 'N/A')}, "
        f"Nombre: {trainee.get('nombre', 'N/A')}, "
        f"Correo: {trainee.get('email', 'N/A')}, "
        f"Ficha: {trainee.get('ficha', 'N/A')}, "
        f"Programa: {trainee.get('programa', 'N/A')}"
    )


def display_confirm_next():
    """Pregunta al usuario si desea registrar otro aprendiz."""


    display_message(
    {
        "type": "info",
        "text": "¿Deseas registrar otro aprendiz? (s/n)",
    }
)

    next_option = input().strip().lower()

    return next_option == "s"

