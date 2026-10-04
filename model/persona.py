class Persona:

    def __init__(self, nombre: str, rut: str):
        self.nombre = nombre
        self.rut = rut

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = valor.strip()

        if len(valor) < 2:
            raise ValueError(
                "El nombre debe tener al menos 2 caracteres."
            )

        self._nombre = valor

    @property
    def rut(self):
        return self._rut

    @rut.setter
    def rut(self, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError(
                "El RUT no puede estar vacío."
            )

        self._rut = valor 