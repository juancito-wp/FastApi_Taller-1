import csv
import json
import os

# ==========================================
# PUNTO 1: CONFIGURACIÓN Y MANEJO DEL ARCHIVO JSON
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
DATA_DIR = os.path.join(BASE_DIR, "data")
JSON_FILE = os.path.join(DATA_DIR, "trainees.json")


def ensure_directory():
    """Crea la carpeta data si aún no existe."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_trainees():
    """Lee y retorna la lista de aprendices desde el archivo JSON."""
    ensure_directory()

    if not os.path.exists(JSON_FILE):
        return []

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_trainees(trainees):
    """Guarda la lista de aprendices en el archivo JSON."""
    ensure_directory()

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(trainees, file, indent=4, ensure_ascii=False)


def search_by_document(document):
    """Busca un aprendiz por su número de documento."""
    trainees = load_trainees()

    for trainee in trainees:
        if trainee.get("documento") == document:
            return trainee

    return None


def register_trainee(data):
    """Agrega un nuevo aprendiz a la lista y guarda los datos."""
    trainees = load_trainees()
    trainees.append(data)
    save_trainees(trainees)


# ==========================================
# PUNTO 3: LÓGICA DE EDICIÓN
# ==========================================


def update_trainee(document, updated_data):
    """Busca un aprendiz por documento y actualiza sus datos."""
    trainees = load_trainees()

    for trainee in trainees:
        if trainee.get("documento") == document:
            trainee.update(updated_data)
            save_trainees(trainees)
            return True

    return False


# ==========================================
# PUNTO 4: ELIMINAR APRENDIZ
# ==========================================


def delete_trainee(document):
    """Elimina un aprendiz usando su número de documento."""
    trainees = load_trainees()
    filtered_trainees = []

    for trainee in trainees:
        if trainee.get("documento") != document:
            filtered_trainees.append(trainee)

    if len(filtered_trainees) < len(trainees):
        save_trainees(filtered_trainees)
        return True

    return False


# ==========================================
# PUNTO 5: BUSCAR APRENDIZ
# ==========================================


def search_trainees_by_term(term):
    """Busca aprendices por nombre o número de ficha."""
    trainees = load_trainees()
    term = str(term).strip().lower()
    results = []

    for trainee in trainees:
        name = str(trainee.get("nombre", "")).lower()
        group = str(trainee.get("ficha", "")).lower()

        if term in name or term == group:
            results.append(trainee)

    return results


# ==========================================
# PUNTO 6: EXPORTAR A CSV
# ==========================================


def export_trainees_to_csv():
    """Exporta la lista de aprendices a un archivo CSV."""
    trainees = load_trainees()

    if not trainees:
        return False, "No hay aprendices registrados para exportar."

    ensure_directory()
    csv_file_path = os.path.join(DATA_DIR, "trainees.csv")

    headers = [
        "documento",
        "nombre",
        "ficha",
        "email",
    ]

    try:
        with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            for trainee in trainees:
                row = {
                    "documento": trainee.get("documento", ""),
                    "nombre": trainee.get("nombre", ""),
                    "ficha": trainee.get("ficha", ""),
                    "email": trainee.get("email", ""),
                }
                writer.writerow(row)

        return True, csv_file_path

    except Exception as error:
        return False, str(error)