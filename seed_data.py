from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["clinica_petcare"]
coleccion = db["pacientes"]

# Limpiar colección antes de precargar
coleccion.delete_many({})

pacientes = [
    {
        "nombre": "Rocky", "especie": "Perro", "raza": "Labrador",
        "edad": 5, "peso": 28.5,
        "fecha_registro": datetime(2024, 3, 15),
        "dueño": {"nombre": "María González", "rut": "15.234.567-8",
                  "telefono": "+56912345678", "email": "maria@mail.com"},
        "historial_consultas": [
            {"fecha": datetime(2024, 6, 10), "motivo": "Vacunación anual",
             "veterinario": "Dr. Pérez", "costo": 25000},
            {"fecha": datetime(2025, 1, 20), "motivo": "Control general",
             "veterinario": "Dra. Soto", "costo": 18000}
        ]
    },
    {
        "nombre": "Luna", "especie": "Gato", "raza": "Siamés",
        "edad": 3, "peso": 4.2,
        "fecha_registro": datetime(2024, 7, 1),
        "dueño": {"nombre": "Pedro Ramírez", "rut": "18.456.789-2",
                  "telefono": "+56987654321", "email": "pedro@mail.com"},
        "historial_consultas": [
            {"fecha": datetime(2025, 2, 5), "motivo": "Esterilización",
             "veterinario": "Dr. Pérez", "costo": 80000}
        ]
    },
    {
        "nombre": "Max", "especie": "Perro", "raza": "Bulldog",
        "edad": 7, "peso": 22.0,
        "fecha_registro": datetime(2023, 11, 20),
        "dueño": {"nombre": "Carla Muñoz", "rut": "12.345.678-9",
                  "telefono": "+56911223344", "email": "carla@mail.com"},
        "historial_consultas": [
            {"fecha": datetime(2024, 5, 12), "motivo": "Problemas respiratorios",
             "veterinario": "Dra. Soto", "costo": 45000},
            {"fecha": datetime(2025, 3, 8), "motivo": "Control post-tratamiento",
             "veterinario": "Dra. Soto", "costo": 20000}
        ]
    },
    {
        "nombre": "Mishi", "especie": "Gato", "raza": "Persa",
        "edad": 2, "peso": 3.8,
        "fecha_registro": datetime(2025, 1, 10),
        "dueño": {"nombre": "Ana Castro", "rut": "19.876.543-1",
                  "telefono": "+56955667788", "email": "ana@mail.com"},
        "historial_consultas": [
            {"fecha": datetime(2025, 4, 1), "motivo": "Limpieza dental",
             "veterinario": "Dr. Pérez", "costo": 35000}
        ]
    },
    {
        "nombre": "Toby", "especie": "Perro", "raza": "Beagle",
        "edad": 4, "peso": 12.5,
        "fecha_registro": datetime(2024, 9, 5),
        "dueño": {"nombre": "Jorge López", "rut": "16.543.210-K",
                  "telefono": "+56944556677", "email": "jorge@mail.com"},
        "historial_consultas": [
            {"fecha": datetime(2025, 2, 14), "motivo": "Desparasitación",
             "veterinario": "Dra. Soto", "costo": 15000}
        ]
    },
    {
        "nombre": "Coco", "especie": "Loro", "raza": "Amazonas",
        "edad": 10, "peso": 0.5,
        "fecha_registro": datetime(2023, 6, 18),
        "dueño": {"nombre": "Sofía Vega", "rut": "13.987.654-3",
                  "telefono": "+56933445566", "email": "sofia@mail.com"},
        "historial_consultas": [
            {"fecha": datetime(2024, 8, 22), "motivo": "Revisión de plumaje",
             "veterinario": "Dr. Pérez", "costo": 22000}
        ]
    },
    {
        "nombre": "Bruno", "especie": "Perro", "raza": "Pastor Alemán",
        "edad": 6, "peso": 35.0,
        "fecha_registro": datetime(2024, 2, 28),
        "dueño": {"nombre": "Luis Torres", "rut": "14.222.333-4",
                  "telefono": "+56977889900", "email": "luis@mail.com"},
        "historial_consultas": [
            {"fecha": datetime(2024, 12, 1), "motivo": "Cirugía menor",
             "veterinario": "Dra. Soto", "costo": 120000},
            {"fecha": datetime(2025, 3, 15), "motivo": "Retiro de puntos",
             "veterinario": "Dra. Soto", "costo": 10000}
        ]
    },
    {
        "nombre": "Nala", "especie": "Gato", "raza": "Angora",
        "edad": 1, "peso": 2.5,
        "fecha_registro": datetime(2025, 4, 20),
        "dueño": {"nombre": "Daniela Pino", "rut": "20.111.222-5",
                  "telefono": "+56922334455", "email": "daniela@mail.com"},
        "historial_consultas": [
            {"fecha": datetime(2025, 4, 25), "motivo": "Primera vacuna",
             "veterinario": "Dr. Pérez", "costo": 18000}
        ]
    }
]

resultado = coleccion.insert_many(pacientes)
print(f"✅ {len(resultado.inserted_ids)} pacientes precargados correctamente.")