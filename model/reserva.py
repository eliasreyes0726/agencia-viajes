from model.excepciones import (
    AnticipoInsuficienteError,
    SinCuposError
)

from model.paquete_internacional import (
    PaqueteInternacional
)


class Reserva:

    def __init__(
        self,
        cliente,
        agente,
        paquete,
        proveedor,
        fecha_viaje,
        precio_paquete_clp,
        anticipo,
        tipo_cambio=1.0
    ):

        self.cliente = cliente
        self.agente = agente
        self.paquete = paquete
        self.proveedor = proveedor

        self.fecha_viaje = fecha_viaje

        self.precio_paquete_clp = float(
            precio_paquete_clp
        )

        self.tipo_cambio = float(
            tipo_cambio
        )

        self.detalles = []

        self.anticipo = anticipo

    @property
    def anticipo(self):
        return self._anticipo

    @anticipo.setter
    def anticipo(
        self,
        valor
    ):

        valor = float(valor)

        if valor < 0:
            raise ValueError(
                "El anticipo no puede ser negativo."
            )

        self._anticipo = valor

    def agregar_detalle(
        self,
        detalle
    ):

        self.detalles.append(
            detalle
        )

    def total(self):

        total_detalles = sum(
            detalle.subtotal()
            for detalle in self.detalles
        )

        return (
            self.precio_paquete_clp
            + total_detalles
        )

    def validar_confirmacion(self):

        # Regla 1:
        # los paquetes internacionales requieren pasaporte
        if isinstance(
            self.paquete,
            PaqueteInternacional
        ):

            if not self.cliente.pasaporte:

                raise ValueError(
                    "Un paquete internacional "
                    "requiere pasaporte válido."
                )

        # Regla 2:
        # no se puede reservar si no hay cupos
        if not self.proveedor.tiene_cupos():

            raise SinCuposError(
                "No se puede confirmar la reserva "
                "porque el proveedor no tiene cupos."
            )

        # Regla 3:
        # anticipo mínimo del 50%
        minimo_anticipo = (
            self.total()
            * 0.50
        )

        if self.anticipo < minimo_anticipo:

            raise AnticipoInsuficienteError(
                "El anticipo debe ser "
                "al menos el 50% del total."
            )

        return True
                               

