from datetime import datetime
import requests
from dao.database import get_connection
from model.excepciones import APITipoCambioError


class TipoCambioService:

    URL = "https://mindicador.cl/api/dolar"

    def obtener_dolar(self):
        try:
            respuesta = requests.get(self.URL, timeout=5)
            respuesta.raise_for_status()
            datos = respuesta.json()
            serie = datos.get("serie", [])
            if not serie:
                raise APITipoCambioError("La API no entregó información de la serie del dólar.")

            valor = float(serie[0]["valor"])
            self._guardar_local(valor)
            return valor

        except Exception as error:
            raise APITipoCambioError(f"Falla en la consulta a la API de tipo de cambio: {error}") from error

    def _guardar_local(self, valor):
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
                    datetime.now().isoformat(timespec="seconds")
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
                ("dolar",)
            )
            fila = cursor.fetchone()
            if fila:
                return float(fila[0])
            return None

    def obtener_dolar_con_fallback(self, valor_defecto=950.0):
        """Intenta obtener el dólar en vivo. Si la API falla, intenta obtener el último valor guardado en SQLite.
        Si no hay registros locales, retorna el valor por defecto provisto."""
        try:
            return self.obtener_dolar()
        except APITipoCambioError as err:
            ultimo = self.ultimo_dolar_guardado()
            if ultimo is not None:
                return ultimo
            return float(valor_defecto)