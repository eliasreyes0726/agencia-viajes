from dao.base_dao import BaseDAO
from dao.database import get_connection
from model.paquete_nacional import PaqueteNacional
from model.paquete_internacional import PaqueteInternacional
from model.paquete_crucero import PaqueteCrucero
from model.excepciones import RecursoNoEncontradoError


class PaqueteDAO(BaseDAO):

    tabla = "paquetes"

    def crear(self, paquete, tipo):
        with get_connection() as conexion:
            cursor = conexion.execute(
                """
                INSERT INTO paquetes(
                    nombre,
                    tipo,
                    precio_base,
                    proveedor_id
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    paquete.nombre,
                    tipo,
                    paquete.precio_base,
                    paquete.proveedor_id
                )
            )
            return cursor.lastrowid

    def actualizar(self, id_, paquete, tipo):
        with get_connection() as conexion:
            cursor = conexion.execute(
                """
                UPDATE paquetes
                SET
                    nombre = ?,
                    tipo = ?,
                    precio_base = ?,
                    proveedor_id = ?
                WHERE id = ?
                """,
                (
                    paquete.nombre,
                    tipo,
                    paquete.precio_base,
                    paquete.proveedor_id,
                    id_
                )
            )
            if cursor.rowcount == 0:
                raise RecursoNoEncontradoError(f"No existe paquete con id {id_}")

    def _mapear_paquete(self, fila):
        id_p, nombre, tipo, precio_base, proveedor_id = fila
        tipo_str = str(tipo).lower().strip()
        if tipo_str == "nacional":
            return PaqueteNacional(id_p, nombre, precio_base, proveedor_id)
        elif tipo_str == "internacional":
            return PaqueteInternacional(id_p, nombre, precio_base, proveedor_id)
        elif tipo_str == "crucero":
            return PaqueteCrucero(id_p, nombre, precio_base, proveedor_id)
        else:
            raise ValueError(f"Tipo de paquete desconocido: {tipo}")

    def obtener_por_id(self, id_):
        with get_connection() as conexion:
            cursor = conexion.execute(
                "SELECT id, nombre, tipo, precio_base, proveedor_id FROM paquetes WHERE id = ?",
                (id_,)
            )
            fila = cursor.fetchone()
            if not fila:
                raise RecursoNoEncontradoError(f"No existe paquete con id {id_}")
            return self._mapear_paquete(fila)

    def listar_todos(self):
        with get_connection() as conexion:
            cursor = conexion.execute(
                "SELECT id, nombre, tipo, precio_base, proveedor_id FROM paquetes ORDER BY id ASC"
            )
            filas = cursor.fetchall()
            return [self._mapear_paquete(f) for f in filas]