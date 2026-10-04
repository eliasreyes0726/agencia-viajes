from datetime import datetime

import requests

from dao.database import get_connection


class TipoCambioService:

    URL = "https://mindicador.cl/api/dolar"

    def obtener_dolar(self):

        try:

            respuesta = requests.get(
                self.URL,
                timeout=5
            )

            respuesta.raise_for_status()

            datos = respuesta.json()

            serie = datos.get(
                "serie",
                []
            )

            if not serie:
                raise ValueError(
                    "La API no entregó información del dólar."
                )

            valor = float(
                serie[0]["valor"]
            )

            self._guardar_local(
                valor
            )

            return valor

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            TypeError
        ) as error:

            print(
                "No fue posible consultar el dólar:"
            )

            print(
                error
            )

            print(
                "El sistema continuará funcionando."
            )

            return None

    def _guardar_local(
        self,
        valor
    ):

        with get_connection() as conexion:

            conexion.execute(
                """
                INSERT INTO indicadores(
                    codigo,
                    valor,
                    fecha_consulta
                )
                VALUES (?, ?, ?)
                """,
                (
                    "dolar",
                    valor,
                    datetime.now().isoformat(
                        timespec="seconds"
                    )
                )
            )

    def ultimo_dolar_guardado(self):

        with get_connection() as conexion:

            cursor = conexion.execute(
                """
                SELECT valor
                FROM indicadores
                WHERE codigo = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (
                    "dolar",
                )
            )

            fila = cursor.fetchone()

            if fila:
                return float(
                    fila[0]
                )

            return None
           