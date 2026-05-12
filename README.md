# 🏥 Clínica Veterinaria PetCare - Sistema CRUD MongoDB

Sistema de gestión de pacientes veterinarios desarrollado en Python + PyMongo.

## Requisitos
- Python 3.10+
- MongoDB local en puerto 27017

## Instalación y ejecución
```bash
pip install -r requirements.txt
python seed_data.py
python main.py
```

## Funcionalidades
1. Crear paciente
2. Listar pacientes
3. Buscar por edad ($gte)
4. Buscar por nombre (regex)
5. Buscar por rango de fechas
6. Buscar en subdoc o array
7. Actualizar peso (raíz)
8. Actualizar subdoc/array
9. Eliminar paciente

### ✨ Cancelación de operaciones

🔙 Dentro de cualquier opción del menú, escribir **`x`** en cualquier campo permite **cancelar la operación y volver al menú principal** sin necesidad de cerrar el programa con `Ctrl + C`.