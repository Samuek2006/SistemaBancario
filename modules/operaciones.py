import modules.corefiles as corafiles
import modules.menu as menu
import modules.utilidades as utilidades
from datetime import datetime
import time

# Archivo donde se guardarán las cuentas
DB_FILE = "data/cuentasBancarias.json"

# Inicializamos el archivo si no existe
corafiles.initialize_json(DB_FILE)

def crear_cuenta():
    """
    Crea una nueva cuenta bancaria y la guarda en el archivo JSON
    """
    utilidades.Limpiar_consola()
    numeroCuenta = input("Ingrese el número de cuenta: ")
    cc = input("Ingrese el número de cédula: ")
    titular = input("Ingrese el nombre del titular: ")
    correo = input("Ingrese el correo electrónico: ")
    edad = int(input("Ingrese la edad: "))
    movil = input("Ingrese el número de celular: ")
    fijo = input("Ingrese el número de teléfono fijo: ")
    pais = input("Ingrese el país: ")
    dep = input("Ingrese el departamento: ")
    ciudad = input("Ingrese la ciudad: ")
    direccion = input("Ingrese la dirección: ")

    # Producto inicial
    idProducto = input("Ingrese un ID para el producto (ej: P001): ")
    producto = menu.menuPortafolio()
    tipoProducto = 'Debito'
    estado = "Activa"

    nueva_cuenta = {
        numeroCuenta: {
            "CC": cc,
            "titular": titular,
            "Correo": correo,
            "Edad": edad,
            "Contacto": {
                "Movil": movil,
                "Fijo": fijo
            },
            "Ubicacion": {
                "Pais": pais,
                "Departamento": dep,
                "Ciudad": ciudad,
                "Direccion": direccion
            },
            "Productos": {
                idProducto: {
                    "NombreProducto": producto,
                    "TipoProducto": tipoProducto,
                    "Saldo": 0,
                    "Estado": estado,
                    "Historial": {}
                }
            }
        }
    }

    corafiles.update_json(DB_FILE, nueva_cuenta, ["cuentasBancarias"])
    print(f"✅ Cuenta {numeroCuenta} creada correctamente.")
    utilidades.Stop()
    utilidades.Limpiar_consola()

def depositar():
    """
    Permite depositar dinero en un producto de una cuenta
    """
    utilidades.Limpiar_consola()
    numeroCuenta = input("Ingrese el número de cuenta: ")
    idProducto = input("Ingrese el ID del producto donde desea depositar: ")
    monto = float(input("Ingrese el monto a depositar: "))

    data = corafiles.read_json(DB_FILE)
    utilidades.Limpiar_consola()

    # Verificamos si existe la cuenta y el producto
    try:
        cuenta = data["cuentasBancarias"][numeroCuenta]
        producto = cuenta["Productos"][idProducto]

        # Actualizamos el saldo
        producto["Saldo"] += monto

        # Registramos en el historial
        producto["Historial"][str(datetime.now())] = f"Depósito de {monto}"

        # Guardamos cambios
        corafiles.write_json(DB_FILE, data)
        print(f"💰 Se depositaron {monto} en el producto {idProducto} de la cuenta {numeroCuenta}.")
        utilidades.Stop()
        utilidades.Limpiar_consola()

    except KeyError:
        print("⚠ La cuenta o el producto no existen.")
        utilidades.Stop()
        utilidades.Limpiar_consola()

def solicitarCredito():
    """
    Permite solicitar un crédito
    """
    utilidades.Limpiar_consola()
    numeroCuenta = input("Ingrese el número de cuenta: ")

    # Leer la base de datos
    data = corafiles.read_json(DB_FILE)

    if numeroCuenta not in data["cuentasBancarias"]:
        print("⚠ La cuenta no existe.")
        utilidades.Stop()
        return

    utilidades.Limpiar_consola()
    print('\n¿Qué tipo de crédito deseas solicitar?')
    producto = menu.menuCreditos()

    # Datos para evaluación
    ingresosMensuales = float(input('Ingresa el total de ingresos mensuales: '))
    montoSolicitado = float(input('Ingresa el monto de crédito solicitado: '))
    plazoMeses = int(input('Ingresa el plazo (meses) para pagar: '))
    utilidades.Limpiar_consola()

    # Calculo del RCI - Relación Cuota Ingresos
    cuota = montoSolicitado / plazoMeses
    RCI = cuota / ingresosMensuales

    if RCI <= 0.4:
        print("✅ Crédito aprobado.")
        utilidades.Stop()
        utilidades.Limpiar_consola()

        # Generar un ID de producto único
        idProducto = str(len(data["cuentasBancarias"][numeroCuenta]["Productos"]) + 1)

        # Registrar el crédito en la cuenta con más información
        data["cuentasBancarias"][numeroCuenta]["Productos"][idProducto] = {
            "NombreProducto": producto,
            "TipoProducto": "credito",
            "MontoOriginal": montoSolicitado,
            "Saldo": montoSolicitado,          # saldo pendiente
            "PlazoMeses": plazoMeses,
            "Cuota": cuota,
            "CuotasRestantes": plazoMeses,
            "Estado": "Activo",
            "Historial": {
                1: {
                    "FechaMovimiento": time.strftime("%Y-%m-%d"),
                    "Valor": montoSolicitado,
                    "TipoMovimiento": "Crédito Aprobado"
                }
            }
        }

        # Guardar cambios en el archivo JSON
        corafiles.write_json(DB_FILE, data)

        print(f"Crédito {producto} creado con ID {idProducto}.")
        print(f"Monto aprobado: {montoSolicitado} | Plazo: {plazoMeses} meses | Cuota mensual: {cuota}")
        utilidades.Stop()
        utilidades.Limpiar_consola()

    else:
        print("❌ No eres apto para el crédito (RCI mayor a 0.4).")
        utilidades.Stop()
        utilidades.Limpiar_consola()

    input("Enter para continuar...")

def retirar():
    """
    Permite retirar dinero en un producto de una cuenta
    """

    utilidades.Limpiar_consola()
    numeroCuenta = input("Ingrese el número de cuenta: ")
    idProducto = input("Ingrese el ID del producto donde desea retirar: ")
    monto = float(input("Ingrese el monto a retirar: "))
    utilidades.Stop()
    utilidades.Limpiar_consola()

    data = corafiles.read_json(DB_FILE)

    try:
        cuenta = data["cuentasBancarias"][numeroCuenta]
        producto = cuenta["Productos"][idProducto]

        # Validar fondos suficientes
        if producto["Saldo"] < monto:
            print("⚠ Fondos insuficientes para realizar el retiro.")
            utilidades.Stop()
            utilidades.Limpiar_consola()
            return

        # Actualizar saldo (ahora sí resta)
        producto["Saldo"] -= monto

        # Registrar en historial
        producto["Historial"][str(datetime.now())] = f"Retiro de {monto}"

        # Guardar cambios
        corafiles.write_json(DB_FILE, data)
        print(f"💸 Se retiraron {monto} del producto {idProducto} de la cuenta {numeroCuenta}.")
        utilidades.Stop()
        utilidades.Limpiar_consola()

    except KeyError:
        print("⚠ La cuenta o el producto no existen.")
        utilidades.Stop()
        utilidades.Limpiar_consola()

def pagoCuota():
    """
    Permite pagar una cuota de un crédito que tenga el usuario
    """
    utilidades.Limpiar_consola()
    numeroCuenta = input("Ingrese el número de cuenta: ")
    idCredito = input("Ingrese el ID del crédito que desea pagar: ")

    data = corafiles.read_json(DB_FILE)

    try:
        cuenta = data["cuentasBancarias"][numeroCuenta]
        credito = cuenta["Productos"][idCredito]

        # Validar que sea crédito
        if credito["TipoProducto"].lower() != "credito":
            print("⚠ El producto seleccionado no es un crédito.")
            utilidades.Stop()
            utilidades.Limpiar_consola()
            return

        # Validar saldo pendiente
        if credito["Saldo"] <= 0:
            print("✅ Este crédito ya está totalmente pagado.")
            utilidades.Stop()
            utilidades.Limpiar_consola()
            return

        # Tomar valor de la cuota
        cuota = credito.get("Cuota", 0)
        if cuota <= 0:
            print("⚠ Este crédito no tiene definida la cuota.")
            utilidades.Stop()
            utilidades.Limpiar_consola()
            return

        # Mostrar productos de débito disponibles
        print("\nProductos disponibles para pagar:")
        productos_debito = {pid: prod for pid, prod in cuenta["Productos"].items()
                            if prod["TipoProducto"].lower() == "debito"}

        if not productos_debito:
            print("⚠ Esta cuenta no tiene productos de débito para pagar el crédito.")
            utilidades.Stop()
            utilidades.Limpiar_consola()
            return

        for pid, prod in productos_debito.items():
            print(f"- {pid}: {prod['NombreProducto']} (Saldo: {prod['Saldo']})")

        idDebito = input("Ingrese el ID del producto de débito para pagar: ")
        productoDebito = productos_debito.get(idDebito)

        if not productoDebito:
            print("⚠ El producto de débito no existe o no es válido.")
            utilidades.Stop()
            utilidades.Limpiar_consola()
            return

        # Validar saldo suficiente
        if productoDebito["Saldo"] < cuota:
            print("⚠ Fondos insuficientes para pagar la cuota.")
            utilidades.Stop()
            utilidades.Limpiar_consola()
            return

        # Descontar de débito
        productoDebito["Saldo"] -= cuota

        # Reducir saldo y cuotas del crédito
        credito["Saldo"] -= cuota
        credito["CuotasRestantes"] -= 1

        # Guardar movimiento en historial
        credito["Historial"][str(datetime.now())] = f"Pago cuota de {cuota}. Cuotas restantes: {credito['CuotasRestantes']}"
        productoDebito["Historial"][str(datetime.now())] = f"Pago de cuota crédito {idCredito} por {cuota}"

        # Guardar cambios
        corafiles.write_json(DB_FILE, data)

        print(f"✅ Pago realizado. Nuevo saldo pendiente del crédito: {credito['Saldo']} | Cuotas restantes: {credito['CuotasRestantes']}")
        utilidades.Stop()
        utilidades.Limpiar_consola()

    except KeyError:
        print("⚠ La cuenta o el producto de crédito no existen.")
        utilidades.Stop()
        utilidades.Limpiar_consola()

def cancelarCuenta():
    """
    Permite cancelar un producto de una cuenta
    """

    utilidades.Limpiar_consola()
    numeroCuenta = input("Ingrese el número de cuenta: ")
    idProducto = input("Ingrese el ID del producto que desea cancelar: ")
    utilidades.Stop()
    utilidades.Limpiar_consola()

    data = corafiles.read_json(DB_FILE)

    try:
        cuenta = data["cuentasBancarias"][numeroCuenta]
        producto = cuenta["Productos"][idProducto]

        # Validar fondos suficientes
        if producto["Saldo"] != 0 or producto["TipoProducto"] == "credito":
            if producto["Saldo"] != 0:
                print("⚠ La cuenta tiene fondos, no puede se Cancelada...")
            elif producto["TipoProducto"] == "credito":
                print('La cuetna no puede ser Cancelada porque es un Credito..')
            utilidades.Stop()
            utilidades.Limpiar_consola()
            return

        # Eliminar el producto
        del cuenta["Productos"][idProducto]

        # Guardar cambios en el JSON
        corafiles.write_json(DB_FILE, data)
        print(f"✅ El producto {idProducto} ha sido cancelado correctamente.")
        utilidades.Stop()
        utilidades.Limpiar_consola()

    except KeyError:
        print("⚠ La cuenta o el producto no existen.")
        utilidades.Stop()
        utilidades.Limpiar_consola()

