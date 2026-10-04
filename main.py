


from model.paquete_nacional import PaqueteNacional
from model.paquete_internacional import PaqueteInternacional
from model.paquete_crucero import PaqueteCrucero


dolar = 950


nacional = PaqueteNacional(
    1,
    "San Pedro de Atacama",
    500000,
    1
)


internacional = PaqueteInternacional(
    2,
    "Miami",
    1000,
    1
)


crucero = PaqueteCrucero(
    3,
    "Crucero Caribe",
    1000,
    1
)


print(
    nacional.calcular_precio_final(dolar)
)

print(
    internacional.calcular_precio_final(dolar)
)

print(
    crucero.calcular_precio_final(dolar)
) 