"""
CLÍNICA VETERINARIA PETCARE
Sistema CRUD con MongoDB + PyMongo
Permite cancelar cualquier operación escribiendo 'x' en cualquier prompt.
"""

from pymongo import MongoClient
from datetime import datetime

# === CONEXIÓN ===
client = MongoClient("mongodb://localhost:27017/")
db = client["clinica_petcare"]
coleccion = db["pacientes"]


# === EXCEPCIÓN PERSONALIZADA PARA CANCELAR ===
class Cancelado(Exception):
    """Se lanza cuando el usuario escribe 'x' para volver al menú."""
    pass


# === HELPERS DE ENTRADA CON CANCELACIÓN ===
def pedir(texto, tipo=str):
    """
    Pide un dato al usuario. Si escribe 'x' (o 'X'), cancela y vuelve al menú.
    tipo puede ser str, int, float.
    """
    while True:
        valor = input(f"{texto} (o 'x' para cancelar): ").strip()
        if valor.lower() == "x":
            raise Cancelado()
        if valor == "":
            print("⚠ No puede estar vacío. Intenta de nuevo.")
            continue
        try:
            return tipo(valor)
        except ValueError:
            print(f"⚠ Valor inválido. Se esperaba {tipo.__name__}.")


def pedir_fecha(texto):
    """Pide una fecha YYYY-MM-DD, permite cancelar con 'x'."""
    while True:
        valor = input(f"{texto} YYYY-MM-DD (o 'x' para cancelar): ").strip()
        if valor.lower() == "x":
            raise Cancelado()
        try:
            return datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            print("⚠ Formato inválido. Usa YYYY-MM-DD (ej: 2025-04-15).")


# === OPERACIONES CRUD ===
def crear_paciente():
    print("\n--- CREAR PACIENTE --- ")
    nombre = pedir("Nombre mascota")
    especie = pedir("Especie")
    raza = pedir("Raza")
    edad = pedir("Edad", int)
    peso = pedir("Peso (kg)", float)

    dueño = {
        "nombre": pedir("Nombre dueño"),
        "rut": pedir("RUT"),
        "telefono": pedir("Teléfono"),
        "email": pedir("Email")
    }

    consulta = {
        "fecha": datetime.now(),
        "motivo": pedir("Motivo consulta"),
        "veterinario": pedir("Veterinario"),
        "costo": pedir("Costo", int)
    }

    doc = {
        "nombre": nombre, "especie": especie, "raza": raza,
        "edad": edad, "peso": peso,
        "fecha_registro": datetime.now(),
        "dueño": dueño,
        "historial_consultas": [consulta]
    }
    res = coleccion.insert_one(doc)
    print(f"✅ Paciente creado con ID: {res.inserted_id}")


def listar_pacientes():
    print("\n--- LISTADO DE PACIENTES ---")
    total = 0
    for p in coleccion.find():
        total += 1
        print(f"🐾 {p['nombre']} ({p['especie']} - {p['raza']}) "
              f"| Edad: {p['edad']} | Dueño: {p['dueño']['nombre']}")
    print(f"\nTotal: {total} pacientes")


def buscar_por_comparacion():
    print("\n--- BUSCAR POR EDAD (>=) ---")
    edad = pedir("Edad mínima", int)
    resultados = list(coleccion.find({"edad": {"$gte": edad}},
                                     {"nombre": 1, "edad": 1, "_id": 0}))
    if not resultados:
        print("Sin resultados.")
    for r in resultados:
        print(r)


def buscar_regex():
    print("\n--- BUSCAR POR NOMBRE (regex) ---")
    patron = pedir("Texto a buscar")
    resultados = list(coleccion.find({"nombre": {"$regex": patron, "$options": "i"}}))
    if not resultados:
        print("Sin resultados.")
    for r in resultados:
        print(f"🔎 {r['nombre']} - {r['especie']}")


def buscar_por_fechas():
    print("\n--- BUSCAR POR RANGO DE FECHAS ---")
    f1 = pedir_fecha("Desde")
    f2 = pedir_fecha("Hasta")
    resultados = list(coleccion.find({"fecha_registro": {"$gte": f1, "$lte": f2}}))
    if not resultados:
        print("Sin resultados.")
    for r in resultados:
        print(f"📅 {r['nombre']} - {r['fecha_registro'].date()}")


def buscar_subdoc_array():
    print("\n--- BUSCAR EN SUBDOC/ARRAY ---")
    print("1. Por nombre del dueño")
    print("2. Por veterinario en historial")
    op = pedir("Opción")
    if op == "1":
        nombre = pedir("Nombre dueño")
        cursor = coleccion.find({"dueño.nombre": {"$regex": nombre, "$options": "i"}})
    elif op == "2":
        vet = pedir("Veterinario")
        cursor = coleccion.find({"historial_consultas.veterinario": vet})
    else:
        print("⚠ Opción inválida.")
        return
    encontrados = False
    for r in cursor:
        encontrados = True
        print(f"➡ {r['nombre']} | Dueño: {r['dueño']['nombre']}")
    if not encontrados:
        print("Sin resultados.")


def actualizar_raiz():
    print("\n--- ACTUALIZAR PESO ---")
    nombre = pedir("Nombre paciente")
    antes = coleccion.find_one({"nombre": nombre})
    if not antes:
        print("❌ No encontrado.")
        return
    print(f"Antes: peso = {antes['peso']}")
    nuevo = pedir("Nuevo peso", float)
    coleccion.update_one({"nombre": nombre}, {"$set": {"peso": nuevo}})
    print(f"Después: peso = {coleccion.find_one({'nombre': nombre})['peso']} ✅")


def actualizar_sub_array():
    print("\n--- ACTUALIZAR SUBDOC/ARRAY ---")
    nombre = pedir("Nombre paciente")
    if not coleccion.find_one({"nombre": nombre}):
        print("❌ No encontrado.")
        return
    print("1. Cambiar teléfono del dueño")
    print("2. Agregar consulta al historial")
    op = pedir("Opción")
    if op == "1":
        tel = pedir("Nuevo teléfono")
        coleccion.update_one({"nombre": nombre}, {"$set": {"dueño.telefono": tel}})
    elif op == "2":
        nueva = {
            "fecha": datetime.now(),
            "motivo": pedir("Motivo"),
            "veterinario": pedir("Veterinario"),
            "costo": pedir("Costo", int)
        }
        coleccion.update_one({"nombre": nombre}, {"$push": {"historial_consultas": nueva}})
    else:
        print("⚠ Opción inválida.")
        return
    print("✅ Actualizado.")


def eliminar_paciente():
    print("\n--- ELIMINAR PACIENTE ---")
    nombre = pedir("Nombre paciente a eliminar")
    doc = coleccion.find_one({"nombre": nombre})
    if not doc:
        print("❌ No encontrado.")
        return
    print(f"Se eliminará: {doc['nombre']} ({doc['especie']})")
    confirma = pedir("Confirmar (s/n)")
    if confirma.lower() == "s":
        coleccion.delete_one({"nombre": nombre})
        print("✅ Eliminado.")
    else:
        print("Operación cancelada.")


# === MENÚ PRINCIPAL ===
def menu():
    opciones = {
        "1": ("Crear paciente", crear_paciente),
        "2": ("Listar pacientes", listar_pacientes),
        "3": ("Buscar por comparación ($gte)", buscar_por_comparacion),
        "4": ("Buscar por regex", buscar_regex),
        "5": ("Buscar por rango de fechas", buscar_por_fechas),
        "6": ("Buscar en subdoc/array", buscar_subdoc_array),
        "7": ("Actualizar campo raíz", actualizar_raiz),
        "8": ("Actualizar subdoc/array", actualizar_sub_array),
        "9": ("Eliminar paciente", eliminar_paciente),
        "0": ("Salir", None)
    }
    while True:
        print("\n========= CLÍNICA PETCARE =========")
        for k, (desc, _) in opciones.items():
            print(f"{k}. {desc}")
        print("(Dentro de cualquier opción, escribe 'x' para cancelar)")
        op = input("Opción: ").strip()
        if op == "0":
            print("👋 Hasta luego.")
            break
        if op in opciones:
            try:
                opciones[op][1]()
            except Cancelado:
                print("↩ Operación cancelada. Volviendo al menú principal...")
            except Exception as e:
                print(f"⚠ Error: {e}")
        else:
            print("⚠ Opción inválida.")


if __name__ == "__main__":
    menu()