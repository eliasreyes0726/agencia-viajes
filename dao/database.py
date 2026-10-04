import sqlite3

from pathlib import Path


DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "agencia.db"
)


def get_connection():

    conexion = sqlite3.connect(
        DB_PATH
    )

    conexion.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conexion

def crear_tablas():

    with get_connection() as conexion:

        conexion.executescript(
            """
            CREATE TABLE IF NOT EXISTS trabajadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                rut TEXT NOT NULL UNIQUE,
                usuario TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                rol TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                rut TEXT NOT NULL UNIQUE,
                pasaporte TEXT
            );

            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cupos INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS paquetes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                precio_base REAL NOT NULL,
                proveedor_id INTEGER NOT NULL,

                FOREIGN KEY(proveedor_id)
                    REFERENCES proveedores(id)
            );

            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                agente_id INTEGER NOT NULL,
                paquete_id INTEGER NOT NULL,
                proveedor_id INTEGER NOT NULL,
                fecha_reserva TEXT NOT NULL,
                fecha_viaje TEXT NOT NULL,
                tipo_cambio REAL NOT NULL,
                precio_paquete_clp REAL NOT NULL,
                anticipo REAL NOT NULL,
                total REAL NOT NULL,
                estado TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS detalle_reserva (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reserva_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,

                FOREIGN KEY(reserva_id)
                    REFERENCES reservas(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS indicadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL,
                valor REAL NOT NULL,
                fecha_consulta TEXT NOT NULL
            );
            """
        )