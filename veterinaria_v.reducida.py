import mysql.connector
from tabulate import tabulate

# ========== CONEXIÓN ==========
def conectar():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="root1024",
        database="veterinaria_db", 
        auth_plugin='mysql_native_password'
        
    )

def ejecutar_consulta(query, params=None, fetch=False, commit=False):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    resultado = cursor.fetchall() if fetch else None
    if commit:
        conn.commit()
    cursor.close()
    conn.close()
    return resultado

# ========== CRUD GENÉRICO ==========
def alta_generico(tabla, campos):
    print(f"\n--- NUEVO {tabla.upper()} ---")
    valores = [input(f"   {campo.capitalize()}: ") for campo in campos]
    placeholders = ", ".join(["%s"] * len(campos))
    ejecutar_consulta(f"INSERT INTO {tabla} ({', '.join(campos)}) VALUES ({placeholders})", valores, commit=True)
    print(f"✅ {tabla[:-1].capitalize()} agregado")

def ver_generico(tabla, campos, join=None):
    print(f"\n--- LISTADO DE {tabla.upper()} ---")
    if join:
        query = f"SELECT {', '.join(campos[0])} FROM {tabla} {join}"
        headers = campos[1]
    else:
        query = f"SELECT {', '.join(campos)} FROM {tabla}"
        headers = [c.upper() for c in campos]
    datos = ejecutar_consulta(query, fetch=True)
    print(tabulate(datos, headers=headers, tablefmt="rounded_grid") if datos else "ℹ️ Sin registros")

def baja_generico(tabla, id_nombre):
    ver_generico(*mapas[tabla]["ver"])
    try:
        id_val = int(input(f"\nID del {tabla[:-1]} a eliminar: "))
        if input(f"¿Eliminar {tabla[:-1]} ID {id_val}? (s/n): ").lower() == "s":
            ejecutar_consulta(f"DELETE FROM {tabla} WHERE {id_nombre} = %s", (id_val,), commit=True)
            print("✅ Eliminado")
        else:
            print("❌ Cancelado")
    except:
        print("❌ ID inválido")

def modificar_generico(tabla, id_nombre, campos):
    ver_generico(*mapas[tabla]["ver"])
    try:
        id_val = int(input(f"\nID del {tabla[:-1]} a modificar: "))
        actualizados = []
        for campo in campos:
            nuevo = input(f"Nuevo {campo} (Enter si no cambia): ")
            if nuevo:
                ejecutar_consulta(f"UPDATE {tabla} SET {campo} = %s WHERE {id_nombre} = %s", (nuevo, id_val), commit=True)
                actualizados.append(campo)
        print("✅ Actualizado" if actualizados else "⚠️ Sin cambios")
    except:
        print("❌ Error")

# ========== MASCOTAS (tiene JOIN) ==========
def ver_mascotas():
    query = """SELECT m.id_mascota, m.nombre, m.especie, m.edad, d.nombre 
               FROM mascotas m JOIN duenos d ON m.id_dueno = d.id_dueno"""
    datos = ejecutar_consulta(query, fetch=True)
    print("\n--- LISTADO DE MASCOTAS ---")
    print(tabulate(datos, headers=["ID", "MASCOTA", "ESPECIE", "EDAD", "DUEÑO"], tablefmt="rounded_grid") if datos else "ℹ️ Sin mascotas")

def alta_mascota():
    duenos = ejecutar_consulta("SELECT id_dueno, nombre FROM duenos", fetch=True)
    if not duenos:
        print("⚠️ Primero registrá un dueño")
        return
    print("\nDueños disponibles:")
    print(tabulate(duenos, headers=["ID", "NOMBRE"], tablefmt="simple"))
    id_dueno = int(input("   ID del dueño: "))
    nombre = input("   Nombre: ")
    especie = input("   Especie: ")
    edad = input("   Edad: ") or None
    ejecutar_consulta("INSERT INTO mascotas (nombre, especie, edad, id_dueno) VALUES (%s, %s, %s, %s)",
                      (nombre, especie, edad, id_dueno), commit=True)
    print(f"✅ Mascota '{nombre}' agregada")

# ========== TURNOS (tiene múltiples JOINs) ==========
def ver_turnos():
    query = """SELECT t.id_turno, m.nombre, v.nombre, t.fecha, t.hora, t.motivo 
               FROM turnos t JOIN mascotas m ON t.id_mascota = m.id_mascota
               JOIN veterinarios v ON t.id_veterinario = v.id_veterinario ORDER BY t.fecha DESC"""
    datos = ejecutar_consulta(query, fetch=True)
    print("\n--- LISTADO DE TURNOS ---")
    print(tabulate(datos, headers=["ID", "MASCOTA", "VETERINARIO", "FECHA", "HORA", "MOTIVO"], tablefmt="rounded_grid") if datos else "ℹ️ Sin turnos")

def alta_turno():
    mascotas = ejecutar_consulta("SELECT id_mascota, nombre FROM mascotas", fetch=True)
    if not mascotas:
        print("⚠️ No hay mascotas")
        return
    vets = ejecutar_consulta("SELECT id_veterinario, nombre FROM veterinarios", fetch=True)
    if not vets:
        print("⚠️ No hay veterinarios")
        return
    print("\nMascotas:", tabulate(mascotas, headers=["ID", "NOMBRE"], tablefmt="simple"), sep="\n")
    id_mascota = int(input("   ID mascota: "))
    print("\nVeterinarios:", tabulate(vets, headers=["ID", "NOMBRE"], tablefmt="simple"), sep="\n")
    id_vet = int(input("   ID veterinario: "))
    fecha = input("   Fecha (YYYY-MM-DD): ")
    hora = input("   Hora (HH:MM:SS): ")
    motivo = input("   Motivo: ")
    ejecutar_consulta("INSERT INTO turnos (id_mascota, id_veterinario, fecha, hora, motivo) VALUES (%s, %s, %s, %s, %s)",
                      (id_mascota, id_vet, fecha, hora, motivo), commit=True)
    print("✅ Turno agendado")

# ========== MAPAS DE CONFIGURACIÓN ==========
mapas = {
    "duenos": {
        "alta": ("duenos", ["nombre", "telefono"]),
        "ver": ("duenos", ["id_dueno", "nombre", "telefono"]),
        "baja": ("duenos", "id_dueno"),
        "mod": ("duenos", "id_dueno", ["nombre", "telefono"])
    },
    "veterinarios": {
        "alta": ("veterinarios", ["nombre", "especialidad"]),
        "ver": ("veterinarios", ["id_veterinario", "nombre", "especialidad"]),
        "baja": ("veterinarios", "id_veterinario"),
        "mod": ("veterinarios", "id_veterinario", ["nombre", "especialidad"])
    }
}

# ========== MENÚS DINÁMICOS ==========
def menu_entidad(nombre, tabla, tiene_alta_especial=False, tiene_ver_especial=False):
    while True:
        print(f"\n{'-'*40}\n  🐾 {nombre.upper()}\n{'-'*40}")
        print("  1. Alta\n  2. Baja\n  3. Modificación\n  4. Ver todos\n  5. Volver")
        op = input("👉 Opción: ")
        if op == "1":
            if tiene_alta_especial:
                alta_mascota() if nombre == "mascotas" else alta_turno()
            else:
                alta_generico(*mapas[tabla]["alta"])
        elif op == "2":
            baja_generico(*mapas[tabla]["baja"])
        elif op == "3":
            modificar_generico(*mapas[tabla]["mod"])
        elif op == "4":
            ver_mascotas() if nombre == "mascotas" else ver_turnos() if nombre == "turnos" else ver_generico(*mapas[tabla]["ver"])
        elif op == "5":
            break
        else:
            print("❌ Opción inválida")
        input("Presioná Enter...")

def menu():
    while True:
        print("\n" + "="*50 + "\n  🐾 VETTURNOS - GESTIÓN VETERINARIA 🐾\n" + "="*50)
        print("  1. 🐕 DUEÑOS\n  2. 🐈 MASCOTAS\n  3. 👨‍⚕️ VETERINARIOS\n  4. 📅 TURNOS\n  5. 🚪 SALIR")
        op = input("👉 Opción: ")
        if op == "1":
            menu_entidad("dueños", "duenos")
        elif op == "2":
            menu_entidad("mascotas", "mascotas", tiene_alta_especial=True)
        elif op == "3":
            menu_entidad("veterinarios", "veterinarios")
        elif op == "4":
            menu_entidad("turnos", "turnos", tiene_alta_especial=True)
        elif op == "5":
            print("\n✅ ¡Gracias por usar VetTurnos!\n")
            break
        else:
            print("\n❌ Opción inválida")
            input("Presioná Enter...")

if __name__ == "__main__":
    menu()