from persistence.db import fetch_all, execute

ESPECIALIDADES = ('carpintero', 'electronica', 'empaque')


class Duende:
    def __init__(self, nombre, especialidad, id_carta_asignada=None, id_duende=None):
        if especialidad not in ESPECIALIDADES:
            raise ValueError('Especialidad invalida')
        self.id_duende = id_duende
        self.nombre = nombre
        self.especialidad = especialidad
        self.id_carta_asignada = id_carta_asignada

    def save(self):
        self.id_duende = execute(
            "INSERT INTO duendes (nombre, especialidad, id_carta_asignada) "
            "VALUES (%s, %s, %s)",
            (self.nombre, self.especialidad, self.id_carta_asignada),
        )
        return self.id_duende

    @staticmethod
    def get_all():
        return fetch_all(
            "SELECT d.*, n.nombre AS nino_asignado "
            "FROM duendes d "
            "LEFT JOIN cartas c ON c.id_carta = d.id_carta_asignada "
            "LEFT JOIN ninos n  ON n.id_nino = c.id_nino "
            "ORDER BY d.nombre")

    @staticmethod
    def asignar(id_duende, id_carta):
        """id_carta vacio/None libera al duende."""
        execute("UPDATE duendes SET id_carta_asignada = %s WHERE id_duende = %s",
                (id_carta or None, id_duende))