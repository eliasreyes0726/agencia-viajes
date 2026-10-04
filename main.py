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
from model.paquete_nacional import PaqueteNacional
from model.detalle_reserva import DetalleReserva
from model.reserva import Reserva, EstadoReserva
from model.excepciones import (
    SinCuposError,
    AnticipoInsuficienteError,
    RecursoNoEncontradoError,
    APITipoCambioError
)

from services.auth_service import crear_hash_password
from services.tipo_cambio_service import TipoCambioService


print("=== INICIANDO PRUEBA COMPLETA DE MEJORAS Y PERSISTENCIA ===")

# 1. Reiniciar y crear tablas de la base de datos
if DB_PATH.exists():
    os.remove(DB_PATH)

crear_tablas()
print("1. Tablas SQLite creadas correctamente.")

# 2. Consultar el Dólar en Vivo desde la API REST con Fallback
tipo_cambio_service = TipoCambioService()
dolar_actual = tipo_cambio_service.obtener_dolar_con_fallback(valor_defecto=950.0)
print(f"2. Valor del Dólar obtenido (API / Fallback): ${dolar_actual:.2f} CLP")

# 3. Crear y Guardar Cliente
cliente_dao = ClienteDAO()
cliente = Cliente("Juan Pérez", "12.345.678-9", "AB123456")
cliente_id = cliente_dao.crear(cliente)
print(f"3. Cliente guardado exitosamente con ID: {cliente_id}")

# 4. Crear y Guardar Proveedor
proveedor_dao = ProveedorDAO()
proveedor = Proveedor(None, "Proveedor Internacional", 5)
proveedor_id = proveedor_dao.crear(proveedor)
proveedor.id_proveedor = proveedor_id
print(f"4. Proveedor guardado con ID: {proveedor_id}")

# 5. Crear y Guardar Trabajador (Agente de Viajes)
trabajador_dao = TrabajadorDAO()
agente = AgenteViajes("María González", "11.111.111-1", "maria.agente", crear_hash_password("ClaveSegura123"))
agente_id = trabajador_dao.crear(agente, "agente")
print(f"5. Agente de Viajes guardado con ID: {agente_id}")

# 6. Crear, Guardar y Probar CRUD en PaqueteDAO
paquete_dao = PaqueteDAO()
paquete_int = PaqueteInternacional(None, "Miami 7 noches", 1000, proveedor_id)
paquete_id = paquete_dao.crear(paquete_int, "internacional")
print(f"6. Paquete Internacional guardado con ID: {paquete_id}")

# Probar lectura en PaqueteDAO
paquete_recuperado = paquete_dao.obtener_por_id(paquete_id)
print(f"   - Paquete recuperado desde DAO: '{paquete_recuperado.nombre}' (Tipo: {type(paquete_recuperado).__name__})")

precio_paquete_clp = paquete_recuperado.calcular_precio_final(tipo_cambio=dolar_actual)
print(f"   - Precio paquete en CLP: ${precio_paquete_clp:,.2f}")

# 7. Crear Reserva con Reglas de Negocio y Estado Enum
reserva = Reserva(
    cliente=cliente,
    agente=agente,
    paquete=paquete_recuperado,
    proveedor=proveedor,
    fecha_viaje="2026-12-15",
    precio_paquete_clp=precio_paquete_clp,
    anticipo=0,
    tipo_cambio=dolar_actual
)

reserva.agregar_detalle(DetalleReserva("hotel", "Hotel 7 noches", 1, 150000))
reserva.agregar_detalle(DetalleReserva("seguro", "Seguro de viaje", 1, 50000))

total_reserva = reserva.total()
print(f"7. Total de la reserva: ${total_reserva:,.2f} CLP")

# Aplicar pago del 50% mínimo para confirmar
reserva.pagar_saldo(total_reserva * 0.50)
print(f"   - Anticipo aplicado: ${reserva.anticipo:,.2f} CLP | Saldo pendiente: ${reserva.saldo_pendiente():,.2f} CLP")

# Validar confirmación
reserva.validar_confirmacion()
print(f"   - Estado de la reserva tras validación: {reserva.estado.value}")

# 8. Guardar Reserva y sus detalles en SQLite
reserva_dao = ReservaDAO()
reserva_id = reserva_dao.crear(reserva, cliente_id, agente_id, paquete_id)
print(f"8. Reserva guardada exitosamente en BD con ID: {reserva_id}")

# 9. Prueba de Captura de Excepciones Específicas
print("9. Probando captura de excepciones propias:")
try:
    paquete_dao.obtener_por_id(999)
except RecursoNoEncontradoError as err:
    print(f"   - Capturada RecursoNoEncontradoError exitosamente: '{err}'")

print("=== PRUEBAS Y VERIFICACIÓN COMPLETADAS CON ÉXITO ===")