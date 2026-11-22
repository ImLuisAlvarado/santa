from persistence.db import fetch_all, fetch_one, execute


class Nino:
    def __init__(self, nombre, direccion, pais, puntos_comportamiento=0, id_nino=None):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del niño es obligatorio.")
        if not direccion or not direccion.strip():
            raise ValueError("La dirección es obligatoria.")
        if not pais or not pais.strip():
            raise ValueError("El país es obligatorio.")

        puntos = int(puntos_comportamiento)
        if puntos < 0 or puntos > 100:
            raise ValueError("Los puntos deben estar entre 0 y 100.")

        self.id_nino = id_nino
        self.nombre = nombre.strip()
        self.direccion = direccion.strip()
        self.pais = pais.strip()
        self.puntos_comportamiento = puntos

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

    @property
    def lista(self):
        return "lista_buena" if self.puntos_comportamiento >= 50 else "lista_mala"

    def update(self):
        if not self.id_nino:
            raise ValueError("No se puede actualizar un niño sin id_nino.")
        return execute(
            "UPDATE ninos "
            "SET nombre = %s, direccion = %s, pais = %s, puntos_comportamiento = %s "
            "WHERE id_nino = %s",
            (
                self.nombre,
                self.direccion,
                self.pais,
                self.puntos_comportamiento,
                self.id_nino,
            ),
        )

    @staticmethod
    def delete(id_nino):
        return execute("DELETE FROM ninos WHERE id_nino = %s", (id_nino,))