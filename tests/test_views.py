from unittest.mock import patch
from src.views import trainee_view


@patch("src.views.trainee_view.trainee_template.display_message")
@patch("src.views.trainee_view.trainee_template.get_trainee_input")
@patch("src.views.trainee_view.trainee_model.register_trainee")
@patch("src.views.trainee_view.trainee_model.search_by_document")
def test_register_trainee_view_success(
    mock_search, mock_register, mock_input, mock_display
):
    # Arrange
    trainee_data = {
        "tipo_doc": "CC",
        "documento": "123456789",
        "nombre": "Juan Perez",
        "ficha": "2023-001",
        "programa": "Programación",
        "email": "juan.perez@gmail.com",
    }
    mock_input.return_value = trainee_data
    mock_search.return_value = None

    # Act
    trainee_view.register_trainee_view()

    # Assert
    mock_input.assert_called_once()

    mock_search.assert_called_once_with(trainee_data["documento"])

    mock_register.assert_called_once_with(trainee_data)

    mock_display.assert_called_once_with(
        {
            "type": "success",
            "text": (
                f"Aprendiz {trainee_data['nombre']} "
                f"registrado exitosamente en la ficha "
                f"{trainee_data['ficha']}."
            ),
        }
    )