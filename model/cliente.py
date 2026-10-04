import re

from model.persona import Persona


class Cliente(Persona):

    def __init__(
        self,
        nombre: str,
        rut: str,
        pasaporte: str | None = None
    ):
        super().__init__(nombre, rut)

        self.pasaporte = pasaporte

    @property
    def pasaporte(self):
        return self._pasaporte

    @pasaporte.setter
    def pasaporte(self, valor):

        if valor is None or valor == "":
            self._pasaporte = None
            return

        valor = valor.strip().upper()

        if not re.fullmatch(
            r"[A-Z0-9]{6,12}",
            valor
        ):
            raise ValueError(
                "Pasaporte inválido. "
                "Debe tener entre 6 y 12 "
                "caracteres alfanuméricos."
            )

        self._pasaporte = valor 