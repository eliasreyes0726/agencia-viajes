from datetime import date

from dao.database import get_connection


class ReservaDAO:

    def crear(
        self,
        reserva,
        cliente_id,
        agente_id,
        paquete_id
    ):
        """
        Guarda una reserva completa junto con sus líneas de detalle.

        La operación se realiza dentro de una transacción:
        - valida la reserva
        - descuenta un cupo
        - guarda la cabecera de la reserva
        - guarda todos los detalles
        - hace commit si todo funciona
        - hace rollback si ocurre un error
        """

        # Primero se validan las reglas de negocio.
        reserva.validar_confirmacion()

        conexion = get_connection()

        try:
            # Inicia la transacción.
            conexion.execute(
                "BEGIN"
            )

            # Descuenta un cupo solo si todavía existe disponibilidad.
            cursor_cupo = conexion.execute(
                """
                UPDATE proveedores
                SET cupos = cupos - 1
                WHERE id = ?
                AND cupos > 0
                """,
                (
                    reserva.proveedor.id_proveedor,
                )
            )

            # Si no se modificó ninguna fila,
            # significa que ya no hay cupos.
            if cursor_cupo.rowcount != 1:
                raise ValueError(
                    "El cupo dejó de estar disponible."
                )

            # Guarda la cabecera de la reserva.
            cursor = conexion.execute(
                """
                INSERT INTO reservas(
                    cliente_id,
                    agente_id,
                    paquete_id,
                    proveedor_id,
                    fecha_reserva,
                    fecha_viaje,
                    tipo_cambio,
                    precio_paquete_clp,
                    anticipo,
                    total,
                    estado
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cliente_id,
                    agente_id,
                    paquete_id,
                    reserva.proveedor.id_proveedor,
                    date.today().isoformat(),
                    reserva.fecha_viaje,
                    reserva.tipo_cambio,
                    reserva.precio_paquete_clp,
                    reserva.anticipo,
                    reserva.total(),
                    "CONFIRMADA"
                )
            )

            # Obtenemos el ID de la reserva recién creada.
            reserva_id = cursor.lastrowid

            # Guarda cada línea de detalle de la reserva.
            for detalle in reserva.detalles:

                conexion.execute(
                    """
                    INSERT INTO detalle_reserva(
                        reserva_id,
                        tipo,
                        descripcion,
                        cantidad,
                        precio_unitario
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        reserva_id,
                        detalle.tipo,
                        detalle.descripcion,
                        detalle.cantidad,
                        detalle.precio_unitario
                    )
                )

            # Si todo salió bien, confirmamos la transacción.
            conexion.commit()

            return reserva_id

        except Exception:
            # Si ocurre cualquier error,
            # se deshacen todos los cambios.
            conexion.rollback()

            raise

        finally:
            # Siempre se cierra la conexión.
            conexion.close()

    def obtener(
        self,
        id_reserva
    ):
        """
        Obtiene una reserva junto con sus líneas de detalle.
        """

        with get_connection() as conexion:

            reserva = conexion.execute(
                """
                SELECT *
                FROM reservas
                WHERE id = ?
                """,
                (
                    id_reserva,
                )
            ).fetchone()

            detalles = conexion.execute(
                """
                SELECT *
                FROM detalle_reserva
                WHERE reserva_id = ?
                """,
                (
                    id_reserva,
                )
            ).fetchall()

            return reserva, detalles

    def listar(self):
        """
        Retorna todas las reservas.
        """

        with get_connection() as conexion:

            cursor = conexion.execute(
                """
                SELECT *
                FROM reservas
                ORDER BY id DESC
                """
            )

            return cursor.fetchall()

    def actualizar_estado(
        self,
        id_reserva,
        estado
    ):
        """
        Permite cambiar el estado de una reserva.
        """

        estados_validos = {
            "CONFIRMADA",
            "CANCELADA"
        }

        estado = estado.upper().strip()

        if estado not in estados_validos:
            raise ValueError(
                "Estado inválido. "
                "Solo puede ser CONFIRMADA o CANCELADA."
            )

        with get_connection() as conexion:

            cursor = conexion.execute(
                """
                UPDATE reservas
                SET estado = ?
                WHERE id = ?
                """,
                (
                    estado,
                    id_reserva
                )
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "No existe una reserva con ese ID."
                )

    def eliminar(
        self,
        id_reserva
    ):
        """
        Elimina una reserva.
        Los detalles también se eliminan si la base
        tiene ON DELETE CASCADE.
        """

        with get_connection() as conexion:

            cursor = conexion.execute(
                """
                DELETE FROM reservas
                WHERE id = ?
                """,
                (
                    id_reserva,
                )
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "No existe una reserva con ese ID."
                )
  