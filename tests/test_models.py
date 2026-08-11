from src.models import trainee_model


def test_search_by_document_found(monkeypatch):
    trainees = [
        {
            "tipo_doc": "CC",
            "documento": "123456789",
            "nombre": "Juan Perez",
            "email": "juan.perez@gmail.com",
            "ficha": "2023-001",
            "programa": "Programación",
        }
    ]
    monkeypatch.setattr(trainee_model, "load_trainees", lambda: trainees)

    result = trainee_model.search_by_document("123456789")

    assert result is not None
    assert result["nombre"] == "Juan Perez"


def test_search_by_document_not_found(monkeypatch):
    trainees = []
    monkeypatch.setattr(trainee_model, "load_trainees", lambda: trainees)

    result = trainee_model.search_by_document("999999999")

    assert result is None


def test_search_trainees_by_name(monkeypatch):
    trainees = [
        {
            "documento": "123456789",
            "nombre": "Juan Perez",
            "email": "juan.perez@gmail.com",
            "ficha": "2023-001",
            "programa": "Programación",
        }
    ]
    monkeypatch.setattr(trainee_model, "load_trainees", lambda: trainees)

    results = trainee_model.search_trainees_by_term("juan")

    assert len(results) == 1
    assert results[0]["nombre"] == "Juan Perez"