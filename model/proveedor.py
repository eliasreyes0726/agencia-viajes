class Proveedor:

    def __init__(
        self,
        id_proveedor,
        nombre,
        cupos
    ):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.cupos = cupos

    @property
    def cupos(self):
        return self._cupos

    @cupos.setter
    def cupos(self, valor):

        valor = int(valor)

        if valor < 0:
            raise ValueError(
                "Los cupos no pueden ser negativos."
            )

        self._cupos = valor

    def tiene_cupos(self):

        return self.cupos > 0