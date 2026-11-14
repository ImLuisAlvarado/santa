from persistence.db import fetch_all, execute
from entities.nino import Nino
from entities.regalo import Regalo

ESTADOS = ('recibida', 'en_taller', 'cargada_en_trineo')


class Carta:
    def __init__(self, id_nino, estado_preparacion='recibida', id_carta=None):
        self.id_carta = id_carta
        self.id_nino = int(id_nino)
        self.estado_preparacion = estado_preparacion

    def save(self):
        self.id_carta = execute(
            "INSERT INTO cartas (id_nino, estado_preparacion) VALUES (%s, %s)",
            (self.id_nino, self.estado_preparacion),
        )
        return self.id_carta

    def agregar_regalo(self, id_regalo, cantidad=1):
        """Agrega un regalo a la carta si el nino tiene los puntos requeridos."""
        nino = Nino.get_by_id(self.id_nino)
        regalo = Regalo.get_by_id(id_regalo)
        if not nino or not regalo:
            raise ValueError('Nino o regalo inexistente')
        if nino['puntos_comportamiento'] < regalo['puntos_comportamiento_requeridos']:
            raise ValueError(
                f"{nino['nombre']} no tiene los puntos requeridos para "
                f"'{regalo['nombre']}'")

        execute(
            "INSERT INTO detalles_carta (id_carta, id_regalo, cantidad) "
            "VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE cantidad = cantidad + VALUES(cantidad)",
            (self.id_carta, int(id_regalo), int(cantidad)),
        )

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM vista_cartas_resumen ORDER BY fecha_recepcion DESC")

    @staticmethod
    def get_detalles(id_carta):
        return fetch_all(
            "SELECT d.id_detalle, r.nombre, r.categoria_juguete, d.cantidad "
            "FROM detalles_carta d JOIN regalos r ON r.id_regalo = d.id_regalo "
            "WHERE d.id_carta = %s", (id_carta,))

    @staticmethod
    def actualizar_estado(id_carta, estado):
        if estado not in ESTADOS:
            raise ValueError('Estado invalido')
        execute("UPDATE cartas SET estado_preparacion = %s WHERE id_carta = %s",
                (estado, id_carta))
