from dao.base_dao import BaseDAO

from dao.database import (
    get_connection
)


class TrabajadorDAO(BaseDAO):

    tabla = "trabajadores"


    def crear(
        self,
        trabajador,
        rol
    ):

        with get_connection() as conexion:

         cursor = conexion.execute(
                    """
                INSERT INTO trabajadores(
                    nombre,
                    rut,
                    usuario,
                    password_hash,
                    rol
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    trabajador.nombre,
                    trabajador.rut,
                    trabajador.usuario,
                    trabajador.password_hash,
                    rol
                )
            )

        return cursor.lastrowid

        def buscar_por_usuario(self, usuario):
       
                with get_connection() as conexion:
                    cursor = conexion.execute(
                """
                SELECT *
                FROM trabajadores
                WHERE usuario = ?
                """,
                (
                    usuario,
                )
            )

        return cursor.fetchone() 