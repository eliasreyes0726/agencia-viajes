from dao.database import crear_tablas

from services.tipo_cambio_service import (
    TipoCambioService
)


crear_tablas()


servicio = TipoCambioService()


dolar = servicio.obtener_dolar()


if dolar is not None:

    print(
        "Dólar actual:",
        dolar
    )

else:

    print(
        "No fue posible "
        "obtener el dólar."
    )