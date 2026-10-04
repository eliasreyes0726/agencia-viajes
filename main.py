import os
from dao.database import crear_tablas, DB_PATH
from dao.cliente_dao import ClienteDAO
from dao.proveedor_dao import ProveedorDAO
from dao.paquete_dao import PaqueteDAO
from dao.trabajador_dao import TrabajadorDAO
from dao.reserva_dao import ReservaDAO

from model.cliente import Cliente
from model.proveedor import Proveedor
from model.agente_viajes import AgenteViajes
from model.paquete_internacional import PaqueteInternacional
from model.detalle_reserva import DetalleReserva
from model.reserva import Reserva

from services.auth_service import crear_hash_password


# 1. Reiniciar y crear tablas
if DB_PATH.exists():
    os.remove(DB_PATH)

crear_tablas()

print("Tablas creadas correctamente.")


# 2. Crear cliente
cliente = Cliente(
    "Juan Pérez",
    "12.345.678-9",
    "AB123456"
)

cliente_dao = ClienteDAO()

cliente_id = cliente_dao.crear(
    cliente
)

print(
    "Cliente guardado con ID:",
    cliente_id
)


# 3. Crear proveedor
proveedor = Proveedor(
    None,
    "Proveedor Internacional",
    5
)

proveedor_dao = ProveedorDAO()

proveedor_id = proveedor_dao.crear(
    proveedor
)

proveedor.id_proveedor = proveedor_id

print(
    "Proveedor guardado con ID:",
    proveedor_id
)


# 4. Crear agente
password_hash = crear_hash_password(
    "ClaveSegura123"
)

agente = AgenteViajes(
    "María González",
    "11.111.111-1",
    "maria.agente",
    password_hash
)

trabajador_dao = TrabajadorDAO()

agente_id = trabajador_dao.crear(
    agente,
    "agente"
)

print(
    "Agente guardado con ID:",
    agente_id
)


# 5. Crear paquete internacional
paquete = PaqueteInternacional(
    None,
    "Miami 7 noches",
    1000,
    proveedor_id
)

paquete_dao = PaqueteDAO()

paquete_id = paquete_dao.crear(
    paquete,
    "internacional"
)

print(
    "Paquete guardado con ID:",
    paquete_id
)


# 6. Para esta prueba usamos un dólar fijo
dolar = 950

precio_paquete = paquete.calcular_precio_final(
    dolar
)

print(
    "Precio paquete:",
    precio_paquete
)


# 7. Crear reserva
reserva = Reserva(
    cliente,
    agente,
    paquete,
    proveedor,
    "2026-12-15",
    precio_paquete,
    0,
    dolar
)


# 8. Agregar detalles
hotel = DetalleReserva(
    "hotel",
    "Hotel 7 noches",
    1,
    150000
)

seguro = DetalleReserva(
    "seguro",
    "Seguro de viaje",
    1,
    50000
)

reserva.agregar_detalle(
    hotel
)

reserva.agregar_detalle(
    seguro
)


# 9. Calcular el total
print(
    "Total reserva:",
    reserva.total()
)


# 10. Pagar exactamente el 50%
reserva.anticipo = (
    reserva.total()
    * 0.50
)

print(
    "Anticipo:",
    reserva.anticipo
)


# 11. Guardar reserva completa
reserva_dao = ReservaDAO()

reserva_id = reserva_dao.crear(
    reserva,
    cliente_id,
    agente_id,
    paquete_id
)

print(
    "Reserva guardada correctamente."
)

print(
    "ID reserva:",
    reserva_id
)


# 12. Leer la reserva y sus detalles
cabecera, detalles = reserva_dao.obtener(
    reserva_id
)

print(
    "Cabecera:",
    cabecera
)

print(
    "Detalles:"
)

for detalle in detalles:
    print(
        detalle
    )