import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('historial_cuenta.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_movimiento TEXT,
    monto REAL,
    nuevo_saldo REAL
)
''')

# Verificar si ya existe un Monto_Base en la base de datos
cursor.execute("SELECT nuevo_saldo FROM movimientos ORDER BY id DESC LIMIT 1")
resultado = cursor.fetchone()

if resultado:
    monto_base = resultado[0]
    print(f"El Monto Base actual en la cuenta es: {monto_base} Bolivares")
else:
    monto_base = float(input("Ingrese el monto base de la cuenta en Bolivares:\n"))
    cursor.execute("INSERT INTO movimientos (tipo_movimiento, monto, nuevo_saldo) VALUES (?, ?, ?)",
                   ("Inicial", monto_base, monto_base))  # Registrar el monto inicial

while True:
    opcion = str(input(
        "Ingrese qué acción desea realizar:\n"
        "Dividir el Monto Base de la cuenta\n"
        "Calcular un egreso de la cuenta\n"
        "Adicionar un ingreso al total de la cuenta\n\n"
    ))

    if opcion.title() == "Dividir":
        Ahorro = monto_base * 0.40
        Necesidades = monto_base * 0.40
        gastos = monto_base * 0.20
        print(f"El resultado sería el siguiente:\n"
              f"Ahorrar: {Ahorro}\n"
              f"Primera Necesidad: {Necesidades}\n"
              f"Gastos personales: {gastos}\n\n\n")

    elif opcion.title() == "Egresar":
        Descontar = float(input("Ingrese el monto a descontar de la cuenta: \n"))
        monto_base -= Descontar
        print(f"El monto total actual en la cuenta es: {monto_base}\n\n\n")
        cursor.execute("INSERT INTO movimientos (tipo_movimiento, monto, nuevo_saldo) VALUES (?, ?, ?)",
                       ("Egreso", Descontar, monto_base))  # Registrar en SQLite

    elif opcion.title() == "Ingresar":
        Ingreso = float(input("Ingrese el monto que va a ingresar: \n"))
        monto_base += Ingreso
        print(f"El monto total actual en la cuenta es: {monto_base}\n\n\n")
        cursor.execute("INSERT INTO movimientos (tipo_movimiento, monto, nuevo_saldo) VALUES (?, ?, ?)",
                       ("Ingreso", Ingreso, monto_base))  # Registrar en SQLite

    else:
        print("Esa no es una acción válida en este sistema")

    # Guardar los cambios en la base de datos
    conn.commit()

# Cerrar la conexión al final del programa (esto se puede hacer 
# al final del ciclo o al salir del programa)
