from persistence.db import fetch_all, fetch_one, execute


class Regalo:
    def __init__(self, nombre, descripcion, categoria_juguete,
                 puntos_comportamiento_requeridos=0, id_regalo=None):
        self.id_regalo = id_regalo
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria_juguete = categoria_juguete
        self.puntos_comportamiento_requeridos = int(puntos_comportamiento_requeridos)

    def save(self):
        self.id_regalo = execute(
            "INSERT INTO regalos (nombre, descripcion, categoria_juguete, "
            "puntos_comportamiento_requeridos) VALUES (%s, %s, %s, %s)",
            (self.nombre, self.descripcion, self.categoria_juguete,
             self.puntos_comportamiento_requeridos),
        )
        return self.id_regalo

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM regalos ORDER BY nombre")

    @staticmethod
    def get_by_id(id_regalo):
        return fetch_one("SELECT * FROM regalos WHERE id_regalo = %s", (id_regalo,))
