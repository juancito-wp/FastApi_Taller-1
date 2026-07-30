import json
import os
import csv

# ==========================================
# PUNTO 1: CONFIGURACIÓN Y MANEJO DEL ARCHIVO JSON
# ==========================================

# Ruta dinámica hacia la carpeta 'data/' en la raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
JSON_FILE = os.path.join(DATA_DIR, 'trainees.json')

def ensure_directory():
    """Crea la carpeta 'data/' si aún no existe."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_trainees():
    """Lee y retorna la lista de aprendices desde el archivo JSON."""
    ensure_directory()
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_trainees(trainees):
    """Guarda la lista de aprendices en el archivo JSON."""
    ensure_directory()
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(trainees, f, indent=4, ensure_ascii=False)

def search_by_document(document):
    """Busca un aprendiz por su documento."""
    trainees = load_trainees()
    for t in trainees:
        if t.get('documento') == document or t.get('document') == document:
            return t
    return None

def register_trainee(data):
    """Agrega un nuevo aprendiz a la lista y guarda."""
    trainees = load_trainees()
    trainees.append(data)
    save_trainees(trainees)

# ==========================================
# PUNTO 3: LÓGICA DE EDICIÓN
# ==========================================

def update_trainee(document, updated_data):
    """Busca un aprendiz por su documento y actualiza sus datos en el JSON."""
    trainees = load_trainees()
    for trainee in trainees:
        if trainee.get('documento') == document or trainee.get('document') == document:
            trainee.update(updated_data)
            save_trainees(trainees)
            return True
    return False

def delete_trainee(document):
    """Elimina un aprendiz de la lista buscando por su documento y actualiza el JSON."""
    trainees = load_trainees()
    
    # Filtramos la lista conservando solo los aprendices que NO coincidan con el documento
    filtered_trainees = [
        t for t in trainees 
        if t.get('documento') != document and t.get('document') != document
    ]
    
    # Si la lista filtrada es más pequeña, significa que se encontró y eliminó a alguien
    if len(filtered_trainees) < len(trainees):
        save_trainees(filtered_trainees)
        return True
        
    return False


def search_trainees_by_term(term):
    """Busca aprendices que coincidan con el nombre o la ficha (criterio parcial o exacto)."""
    trainees = load_trainees()
    term = str(term).strip().lower()
    results = []

    for t in trainees:
        # Obtenemos valores contemplando ambas llaves (español o inglés)
        name = str(t.get('nombre') or t.get('name') or '').lower()
        group = str(t.get('ficha') or t.get('group') or '').lower()

        # Comprobamos si el término de búsqueda está en el nombre o en la ficha
        if term in name or term == group:
            results.append(t)

    return results


def export_trainees_to_csv():
    """Exporta la lista de aprendices guardada en JSON a un archivo CSV en la carpeta data/."""
    trainees = load_trainees()
    
    if not trainees:
        return False, "No hay aprendices registrados para exportar."

    csv_file_path = os.path.join(DATA_DIR, 'trainees.csv')
    
    # Definimos los campos estándar del archivo CSV
    headers = ['documento', 'nombre', 'ficha', 'email']

    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for t in trainees:
                # Normalizamos las llaves por si algunas están en inglés o español
                row = {
                    'documento': t.get('documento') or t.get('document') or '',
                    'nombre': t.get('nombre') or t.get('name') or '',
                    'ficha': t.get('ficha') or t.get('group') or '',
                    'email': t.get('email') or ''
                }
                writer.writerow(row)

        return True, csv_file_path
    except Exception as e:
        return False, str(e)