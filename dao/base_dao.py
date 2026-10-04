from dao.database import (
    get_connection
)


class BaseDAO:

    tabla = None


    def listar(self):

        with get_connection() as conexion:

            cursor = conexion.execute(
                f"SELECT * FROM {self.tabla}"
            )

            return cursor.fetchall()


    def obtener(
        self,
        id_
    ):

        with get_connection() as conexion:

            cursor = conexion.execute(
                f"""
                SELECT *
                FROM {self.tabla}
                WHERE id = ?
                """,
                (
                    id_,
                )
            )

            return cursor.fetchone()


    def eliminar(
        self,
        id_
    ):

        with get_connection() as conexion:

            conexion.execute(
                f"""
                DELETE FROM {self.tabla}
                WHERE id = ?
                """,
                (
                    id_,
                )
            ) 