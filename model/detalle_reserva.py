class DetalleReserva:

    TIPOS_VALIDOS = {
        "vuelo",
        "hotel",
        "seguro",
        "excursion"
    }

    def __init__(
        self,
        tipo,
        descripcion,
        cantidad,
        precio_unitario
    ):
        self.tipo = tipo
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):

        valor = valor.strip().lower()

        if valor not in self.TIPOS_VALIDOS:

            raise ValueError(
                "Tipo de detalle inválido."
            )

        self._tipo = valor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):

        valor = int(valor)

        if valor <= 0:

            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        self._cantidad = valor

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(
        self,
        valor
    ):

        valor = float(valor)

        if valor < 0:

            raise ValueError(
                "El precio no puede ser negativo."
            )

        self._precio_unitario = valor

    def subtotal(self):

        return (
            self.cantidad
            * self.precio_unitario
        ) 