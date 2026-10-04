import hashlib
import hmac
import os


def crear_hash_password(password: str) -> str:

    if len(password) < 8:
        raise ValueError(
            "La contraseña debe tener al menos 8 caracteres."
        )

    salt = os.urandom(16)

    derivada = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000
    )

    return (
        f"{salt.hex()}:"
        f"{derivada.hex()}"
    )


def verificar_password(
    password: str,
    almacenado: str
) -> bool:

    try:

        salt_hex, hash_hex = almacenado.split(
            ":",
            1
        )

        derivada = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            200_000
        )

        return hmac.compare_digest(
            derivada.hex(),
            hash_hex
        )

    except (
        ValueError,
        TypeError
    ):

        return False