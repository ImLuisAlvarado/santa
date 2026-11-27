import os
from unittest.mock import patch
import pytest
from flask import Flask
from entities.carta import Carta
from routes.cartas import routes_cartas

@pytest.fixture
def client():
    template_dir = os.path.abspath("templates")
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = "test_secret_key"
    app.config["TESTING"] = True
    routes_cartas(app)
    with app.test_client() as test_client:
        yield test_client

@patch("entities.carta.execute", return_value=10)
def test_save_carta(mock_execute):
    carta = Carta(id_nino=1)
    id_generado = carta.save()

    assert id_generado == 10
    assert carta.id_carta == 10
    mock_execute.assert_called_once()

@patch("entities.carta.execute")
@patch("entities.carta.Regalo.get_by_id")
@patch("entities.carta.Nino.get_by_id")
def test_agregar_regalo_exitoso(mock_nino, mock_regalo, mock_execute):
    mock_nino.return_value = {"id_nino": 1, "nombre": "Manuel", "puntos_comportamiento": 90}
    mock_regalo.return_value = {"id_regalo": 1, "nombre": "Bicicleta", "puntos_comportamiento_requeridos": 60}

    carta = Carta(id_nino=1, id_carta=5)
    carta.agregar_regalo(id_regalo=1, cantidad=2)

    mock_execute.assert_called_once()

@patch("entities.carta.execute")
@patch("entities.carta.Regalo.get_by_id")
@patch("entities.carta.Nino.get_by_id")
def test_agregar_regalo_puntos_insuficientes(mock_nino, mock_regalo, mock_execute):
    mock_nino.return_value = {"id_nino": 2, "nombre": "Manolo", "puntos_comportamiento": 35}
    mock_regalo.return_value = {"id_regalo": 1, "nombre": "Bicicleta", "puntos_comportamiento_requeridos": 60}

    carta = Carta(id_nino=2, id_carta=6)
    with pytest.raises(ValueError, match="no tiene los puntos requeridos"):
        carta.agregar_regalo(id_regalo=1, cantidad=1)

    mock_execute.assert_not_called()


@patch("entities.carta.Regalo.get_by_id", return_value=None)
@patch("entities.carta.Nino.get_by_id", return_value=None)
def test_agregar_regalo_inexistente(mock_nino, mock_regalo):
    carta = Carta(id_nino=99, id_carta=1)
    with pytest.raises(ValueError, match="Nino o regalo inexistente"):
        carta.agregar_regalo(id_regalo=99)


@patch("entities.carta.execute")
def test_actualizar_estado_valido(mock_execute):
    Carta.actualizar_estado(1, "en_taller")
    mock_execute.assert_called_once()


@patch("entities.carta.execute")
def test_actualizar_estado_invalido(mock_execute):
    with pytest.raises(ValueError, match="Estado invalido"):
        Carta.actualizar_estado(1, "perdida_en_la_nieve")
    mock_execute.assert_not_called()


@patch("entities.carta.execute")
def test_eliminar_regalo_y_carta(mock_execute):
    Carta.eliminar_regalo(15)
    Carta.delete(3)
    assert mock_execute.call_count == 2

@patch("routes.cartas.Regalo.get_all", return_value=[])
@patch("routes.cartas.Nino.get_all", return_value=[])
@patch("routes.cartas.Carta.get_all", return_value=[])
def test_get_lista_cartas(mock_cartas, mock_ninos, mock_regalos, client):
    response = client.get("/cartas")
    assert response.status_code == 200


@patch("routes.cartas.Regalo.get_all", return_value=[])
@patch("routes.cartas.Carta.get_detalles", return_value=[])
@patch("routes.cartas.Carta.get_by_id")
def test_get_detalle_carta(mock_get_by_id, mock_detalles, mock_regalos, client):
    mock_get_by_id.return_value = {
        "id_carta": 1,
        "id_nino": 1,
        "nombre": "Manuel Manitas",
        "puntos_comportamiento": 90,
        "lista": "lista_buena",
        "fecha_recepcion": "2026-11-01",
        "estado_preparacion": "en_taller",
    }
    response = client.get("/cartas/1")
    assert response.status_code == 200


@patch("routes.cartas.Carta.agregar_regalo")
@patch("routes.cartas.Carta.save", return_value=4)
def test_post_crear_carta_con_regalo(mock_save, mock_agregar, client):
    response = client.post("/carta", data={"id_nino": "1", "id_regalo": "2", "cantidad": "1"})
    assert response.status_code == 302
    mock_save.assert_called_once()
    mock_agregar.assert_called_once()


@patch("routes.cartas.Carta.actualizar_estado")
def test_post_actualizar_estado(mock_actualizar, client):
    response = client.post("/carta/1/estado", data={"estado_preparacion": "cargada_en_trineo"})
    assert response.status_code == 302
    mock_actualizar.assert_called_once_with(1, "cargada_en_trineo")

@patch("entities.carta.fetch_all", return_value=[{"id_carta": 1, "nino": "Manuel"}])
def test_get_all_cartas(mock_fetch):
    resultado = Carta.get_all()
    assert len(resultado) == 1
    assert resultado[0]["nino"] == "Manuel"
    mock_fetch.assert_called_once()


@patch("entities.carta.fetch_all", return_value=[{"id_detalle": 1, "nombre": "Bicicleta roja", "cantidad": 1}])
def test_get_detalles_carta(mock_fetch):
    detalles = Carta.get_detalles(1)
    assert len(detalles) == 1
    assert detalles[0]["nombre"] == "Bicicleta roja"
    mock_fetch.assert_called_once()


@patch("entities.carta.fetch_one", return_value={"id_carta": 1, "id_nino": 1, "nombre": "Manuel"})
def test_get_by_id_carta(mock_fetch):
    carta = Carta.get_by_id(1)
    assert carta["id_carta"] == 1
    assert carta["id_nino"] == 1
    mock_fetch.assert_called_once()

@patch("routes.cartas.Carta.agregar_regalo")
@patch("routes.cartas.Carta.get_by_id", return_value={"id_carta": 1, "id_nino": 1})
def test_post_add_regalo_a_carta_existente(mock_get_by_id, mock_agregar, client):
    response = client.post("/carta/1/regalo", data={"id_regalo": "2", "cantidad": "3"})
    assert response.status_code == 302
    mock_agregar.assert_called_once_with("2", "3")


@patch("routes.cartas.Carta.agregar_regalo", side_effect=ValueError("Puntos insuficientes"))
@patch("routes.cartas.Carta.get_by_id", return_value={"id_carta": 1, "id_nino": 2})
def test_post_add_regalo_error_puntos_redirige(mock_get_by_id, mock_agregar, client):
    response = client.post("/carta/1/regalo", data={"id_regalo": "1", "cantidad": "1"})
    assert response.status_code == 302


@patch("routes.cartas.Carta.eliminar_regalo")
def test_post_eliminar_regalo_de_carta(mock_eliminar, client):
    response = client.post("/carta/1/regalo/15/eliminar")
    assert response.status_code == 302
    mock_eliminar.assert_called_once_with(15)


@patch("routes.cartas.Carta.delete")
def test_post_eliminar_carta(mock_delete, client):
    response = client.post("/carta/1/eliminar")
    assert response.status_code == 302
    mock_delete.assert_called_once_with(1)