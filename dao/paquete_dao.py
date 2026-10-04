from dao.base_dao import BaseDAO

from dao.database import (
    get_connection
)


class PaqueteDAO(BaseDAO):

    tabla = "paquetes"


    def crear(
        self,
        paquete,
        tipo
    ):

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

    def actualizar(
        self,
        id_,
        paquete,
        tipo
    ):

        with get_connection() as conexion:

            conexion.execute(
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
                    