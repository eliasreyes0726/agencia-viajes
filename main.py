from model.cliente import Cliente


try:
    cliente = Cliente(
        "Juan Pérez",
        "12.345.678-9",
        "AB123456"
    )

    print("Cliente creado correctamente")
    print("Nombre:", cliente.nombre)
    print("RUT:", cliente.rut)
    print("Pasaporte:", cliente.pasaporte)

except ValueError as error:
    print("Dato rechazado:")
    print(error)