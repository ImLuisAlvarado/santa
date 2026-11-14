from persistence.db import fetch_all, fetch_one, execute


class Nino:
    def __init__(self, nombre, direccion, pais, puntos_comportamiento=0, id_nino=None):
        self.id_nino = id_nino
        self.nombre = nombre
        self.direccion = direccion
        self.pais = pais
        self.puntos_comportamiento = int(puntos_comportamiento)

    def save(self):
        self.id_nino = execute(
            "INSERT INTO ninos (nombre, direccion, pais, puntos_comportamiento) "
            "VALUES (%s, %s, %s, %s)",
            (self.nombre, self.direccion, self.pais, self.puntos_comportamiento),
        )
        return self.id_nino

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM ninos ORDER BY nombre")

    @staticmethod
    def get_by_id(id_nino):
        return fetch_one("SELECT * FROM ninos WHERE id_nino = %s", (id_nino,))