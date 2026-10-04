from dao.base_dao import BaseDAO

from dao.database import (
    get_connection
)


class ProveedorDAO(BaseDAO):

    tabla = "proveedores"


    def crear(
        self,
        proveedor
    ):

        with get_connection() as conexion:

            cursor = conexion.execute(
                """
                INSERT INTO proveedores(
                    nombre,
                    cupos
                )
                VALUES (?, ?)
                """,
                (
                    proveedor.nombre,
                    proveedor.cupos
                )
            )

            return cursor.lastrowid


    def actualizar(
        self,
        id_,
        proveedor
    ):

        with get_connection() as conexion:

            conexion.execute(
                """
                UPDATE proveedores
                SET
                    nombre = ?,
                    cupos = ?
                WHERE id = ?
                """,
                (
                    proveedor.nombre,
                    proveedor.cupos,
                    id_
                )
            ) 