from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["clinica_petcare"]
coleccion = db["pacientes"]


def crear_paciente():
    print("\n--- CREAR PACIENTE ---")
    nombre = input("Nombre mascota: ")
    especie = input("Especie: ")
    raza = input("Raza: ")
    edad = int(input("Edad: "))
    peso = float(input("Peso (kg): "))

    print("-- Datos del dueño --")
    dueño = {
        "nombre": input("Nombre dueño: "),
        "rut": input("RUT: "),
        "telefono": input("Teléfono: "),
        "email": input("Email: ")
    }

    print("-- Primera consulta --")
    consulta = {
        "fecha": datetime.now(),
        "motivo": input("Motivo: "),
        "veterinario": input("Veterinario: "),
        "costo": int(input("Costo: "))
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
    for p in coleccion.find():
        print(f"\n🐾 {p['nombre']} ({p['especie']} - {p['raza']}) "
              f"| Edad: {p['edad']} | Dueño: {p['dueño']['nombre']}")
        print(f"   Consultas: {len(p['historial_consultas'])} | ID: {p['_id']}")


def buscar_por_comparacion():
    print("\n--- BÚSQUEDA POR OPERADOR DE COMPARACIÓN ---")
    edad_min = int(input("Edad mínima ($gte): "))
    resultados = coleccion.find(
        {"edad": {"$gte": edad_min}},
        {"nombre": 1, "especie": 1, "edad": 1, "peso": 1, "_id": 0}
    )
    for r in resultados:
        print(r)


def buscar_regex():
    print("\n--- BÚSQUEDA POR REGEX ---")
    patron = input("Texto a buscar en nombre (ej: 'lu'): ")
    resultados = coleccion.find({"nombre": {"$regex": patron, "$options": "i"}})
    for r in resultados:
        print(f"🔎 {r['nombre']} - {r['especie']}")


def buscar_por_fechas():
    print("\n--- BÚSQUEDA POR RANGO DE FECHAS ---")
    desde = input("Fecha desde (YYYY-MM-DD): ")
    hasta = input("Fecha hasta (YYYY-MM-DD): ")
    f1 = datetime.strptime(desde, "%Y-%m-%d")
    f2 = datetime.strptime(hasta, "%Y-%m-%d")
    resultados = coleccion.find({"fecha_registro": {"$gte": f1, "$lte": f2}})
    for r in resultados:
        print(f"📅 {r['nombre']} - registrado: {r['fecha_registro'].date()}")


def buscar_en_subdoc_o_array():
    print("\n--- BÚSQUEDA EN SUBDOC / ARRAY ---")
    print("1. Por nombre del dueño (subdoc)")
    print("2. Por veterinario en historial (array)")
    op = input("Opción: ")
    if op == "1":
        nombre = input("Nombre del dueño: ")
        resultados = coleccion.find({"dueño.nombre": {"$regex": nombre, "$options": "i"}})
    else:
        vet = input("Veterinario: ")
        resultados = coleccion.find({"historial_consultas.veterinario": vet})
    for r in resultados:
        print(f"➡ {r['nombre']} | Dueño: {r['dueño']['nombre']}")


def actualizar_raiz():
    print("\n--- ACTUALIZAR CAMPO RAÍZ ---")
    nombre = input("Nombre del paciente: ")
    antes = coleccion.find_one({"nombre": nombre})
    if not antes:
        print("❌ No encontrado.")
        return
    print(f"Antes: peso = {antes['peso']}")
    nuevo_peso = float(input("Nuevo peso: "))
    coleccion.update_one({"nombre": nombre}, {"$set": {"peso": nuevo_peso}})
    despues = coleccion.find_one({"nombre": nombre})
    print(f"Después: peso = {despues['peso']} ✅")


def actualizar_subdoc_o_array():
    print("\n--- ACTUALIZAR SUBDOC / ARRAY ---")
    nombre = input("Nombre del paciente: ")
    print("1. Cambiar teléfono del dueño (subdoc)")
    print("2. Agregar nueva consulta al historial (array - $push)")
    op = input("Opción: ")
    if op == "1":
        tel = input("Nuevo teléfono: ")
        coleccion.update_one({"nombre": nombre},
                             {"$set": {"dueño.telefono": tel}})
    else:
        nueva = {
            "fecha": datetime.now(),
            "motivo": input("Motivo: "),
            "veterinario": input("Veterinario: "),
            "costo": int(input("Costo: "))
        }
        coleccion.update_one({"nombre": nombre},
                             {"$push": {"historial_consultas": nueva}})
    print("✅ Actualización realizada.")


def eliminar_paciente():
    print("\n--- ELIMINAR PACIENTE ---")
    nombre = input("Nombre del paciente a eliminar: ")
    doc = coleccion.find_one({"nombre": nombre})
    if not doc:
        print("❌ No encontrado.")
        return
    print(f"Se eliminará: {doc['nombre']} ({doc['especie']})")
    if input("Confirmar (s/n): ").lower() == "s":
        res = coleccion.delete_one({"nombre": nombre})
        print(f"✅ Eliminados: {res.deleted_count}")


def menu():
    opciones = {
        "1": ("Crear paciente", crear_paciente),
        "2": ("Listar pacientes", listar_pacientes),
        "3": ("Buscar por comparación ($gte)", buscar_por_comparacion),
        "4": ("Buscar por regex", buscar_regex),
        "5": ("Buscar por rango de fechas", buscar_por_fechas),
        "6": ("Buscar en subdoc/array", buscar_en_subdoc_o_array),
        "7": ("Actualizar campo raíz", actualizar_raiz),
        "8": ("Actualizar subdoc/array", actualizar_subdoc_o_array),
        "9": ("Eliminar paciente", eliminar_paciente),
        "0": ("Salir", None)
    }
    while True:
        print("\n========= CLÍNICA PETCARE =========")
        for k, (desc, _) in opciones.items():
            print(f"{k}. {desc}")
        op = input("Opción: ")
        if op == "0":
            print("👋 Hasta luego.")
            break
        if op in opciones:
            try:
                opciones[op][1]()
            except Exception as e:
                print(f"⚠ Error: {e}")
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()