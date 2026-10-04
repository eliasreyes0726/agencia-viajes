from dao.base_dao import BaseDAO

from dao.database import (
    get_connection
)


class ClienteDAO(BaseDAO):

    tabla = "clientes"


    def crear(
        self,
        cliente
    ):

        with get_connection() as conexion:

            cursor = conexion.execute(
                """
                INSERT INTO clientes(
                    nombre,
                    rut,
                    pasaporte
                )
                VALUES (?, ?, ?)
                """,
                (
                    cliente.nombre,
                    cliente.rut,
                    cliente.pasaporte
                )
            )

            return cursor.lastrowid


    def actualizar(
        self,
        id_,
        cliente
    ):

        with get_connection() as conexion:

            conexion.execute(
                """
                UPDATE clientes
                SET
                    nombre = ?,
                    rut = ?,
                    pasaporte = ?
                WHERE id = ?
                """,
                (
                    cliente.nombre,
                    cliente.rut,
                    cliente.pasaporte,
                    id_
                )
            ) 