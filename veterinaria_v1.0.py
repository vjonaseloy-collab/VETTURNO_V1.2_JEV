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

# ========== MENÚ PRINCIPAL ==========
def menu():
    while True:
        print("\n" + "=" * 50)
        print("  🐾 VETTURNOS - GESTIÓN VETERINARIA 🐾")
        print("=" * 50)
        print("  1. 🐕 DUEÑOS")
        print("  2. 🐈 MASCOTAS")
        print("  3. 👨‍⚕️ VETERINARIOS")
        print("  4. 📅 TURNOS")
        print("  5. 🚪 SALIR")
        print("-" * 50)
        
        op = input("👉 Opción: ")
        
        if op == "1":
            menu_duenos()
        elif op == "2":
            menu_mascotas()
        elif op == "3":
            menu_veterinarios()
        elif op == "4":
            menu_turnos()
        elif op == "5":
            print("\n✅ ¡Gracias por usar VetTurnos!\n")
            break
        else:
            print("\n❌ Opción inválida")
            input("Presioná Enter para continuar...")

# ========== DUEÑOS ==========
def menu_duenos():
    while True:
        print("\n" + "-" * 40)
        print("  🐕 GESTIÓN DE DUEÑOS")
        print("-" * 40)
        print("  1. Alta")
        print("  2. Baja")
        print("  3. Modificación")
        print("  4. Ver todos")
        print("  5. Volver")
        
        op = input("👉 Opción: ")
        
        if op == "1":
            alta_dueno()
        elif op == "2":
            baja_dueno()
        elif op == "3":
            modificar_dueno()
        elif op == "4":
            ver_duenos()
        elif op == "5":
            break
        else:
            print("❌ Opción inválida")
            input("Presioná Enter...")

def alta_dueno():
    print("\n--- NUEVO DUEÑO ---")
    nombre = input("   Nombre: ")
    telefono = input("   Teléfono: ")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO duenos (nombre, telefono) VALUES (%s, %s)", (nombre, telefono))
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Dueño '{nombre}' agregado")
    input("Presioná Enter...")

def ver_duenos():
    print("\n--- LISTADO DE DUEÑOS ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_dueno, nombre, telefono FROM duenos")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if datos:
        print(tabulate(datos, headers=["ID", "NOMBRE", "TELÉFONO"], tablefmt="rounded_grid"))
    else:
        print("ℹ️ No hay dueños registrados")
    input("Presioná Enter...")

def baja_dueno():
    ver_duenos()
    try:
        id_dueno = int(input("\nID del dueño a eliminar: "))
        confirmar = input(f"¿Eliminar dueño ID {id_dueno}? (s/n): ").lower()
        if confirmar == "s":
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM duenos WHERE id_dueno = %s", (id_dueno,))
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Dueño eliminado")
        else:
            print("❌ Cancelado")
    except:
        print("❌ ID inválido")
    input("Presioná Enter...")

def modificar_dueno():
    ver_duenos()
    try:
        id_dueno = int(input("\nID del dueño a modificar: "))
        nuevo_nombre = input("Nuevo nombre (Enter si no cambia): ")
        nuevo_telefono = input("Nuevo teléfono (Enter si no cambia): ")
        
        conn = conectar()
        cursor = conn.cursor()
        if nuevo_nombre:
            cursor.execute("UPDATE duenos SET nombre = %s WHERE id_dueno = %s", (nuevo_nombre, id_dueno))
        if nuevo_telefono:
            cursor.execute("UPDATE duenos SET telefono = %s WHERE id_dueno = %s", (nuevo_telefono, id_dueno))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Dueño actualizado")
    except:
        print("❌ Error")
    input("Presioná Enter...")

# ========== MASCOTAS ==========
def menu_mascotas():
    while True:
        print("\n" + "-" * 40)
        print("  🐈 GESTIÓN DE MASCOTAS")
        print("-" * 40)
        print("  1. Alta")
        print("  2. Baja")
        print("  3. Modificación")
        print("  4. Ver todas")
        print("  5. Volver")
        
        op = input("👉 Opción: ")
        
        if op == "1":
            alta_mascota()
        elif op == "2":
            baja_mascota()
        elif op == "3":
            modificar_mascota()
        elif op == "4":
            ver_mascotas()
        elif op == "5":
            break
        else:
            print("❌ Opción inválida")
            input("Presioná Enter...")

def alta_mascota():
    print("\n--- NUEVA MASCOTA ---")
    
    # Mostrar dueños para elegir
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_dueno, nombre FROM duenos")
    duenos = cursor.fetchall()
    
    if not duenos:
        print("⚠️ Primero registrá un dueño")
        cursor.close()
        conn.close()
        input("Presioná Enter...")
        return
    
    print("\nDueños disponibles:")
    print(tabulate(duenos, headers=["ID", "NOMBRE"], tablefmt="simple"))
    
    id_dueno = int(input("   ID del dueño: "))
    nombre = input("   Nombre de la mascota: ")
    especie = input("   Especie: ")
    edad = input("   Edad: ")
    
    cursor.execute("INSERT INTO mascotas (nombre, especie, edad, id_dueno) VALUES (%s, %s, %s, %s)",
                   (nombre, especie, edad if edad else None, id_dueno))
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Mascota '{nombre}' agregada")
    input("Presioná Enter...")

def ver_mascotas():
    print("\n--- LISTADO DE MASCOTAS ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id_mascota, m.nombre, m.especie, m.edad, d.nombre
        FROM mascotas m
        JOIN duenos d ON m.id_dueno = d.id_dueno
    """)
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if datos:
        print(tabulate(datos, headers=["ID", "MASCOTA", "ESPECIE", "EDAD", "DUEÑO"], tablefmt="rounded_grid"))
    else:
        print("ℹ️ No hay mascotas registradas")
    input("Presioná Enter...")

def baja_mascota():
    ver_mascotas()
    try:
        id_mascota = int(input("\nID de la mascota a eliminar: "))
        confirmar = input(f"¿Eliminar mascota ID {id_mascota}? (s/n): ").lower()
        if confirmar == "s":
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mascotas WHERE id_mascota = %s", (id_mascota,))
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Mascota eliminada")
        else:
            print("❌ Cancelado")
    except:
        print("❌ ID inválido")
    input("Presioná Enter...")

def modificar_mascota():
    ver_mascotas()
    try:
        id_mascota = int(input("\nID de la mascota a modificar: "))
        nuevo_nombre = input("Nuevo nombre (Enter si no cambia): ")
        nueva_especie = input("Nueva especie (Enter si no cambia): ")
        nueva_edad = input("Nueva edad (Enter si no cambia): ")
        
        conn = conectar()
        cursor = conn.cursor()
        if nuevo_nombre:
            cursor.execute("UPDATE mascotas SET nombre = %s WHERE id_mascota = %s", (nuevo_nombre, id_mascota))
        if nueva_especie:
            cursor.execute("UPDATE mascotas SET especie = %s WHERE id_mascota = %s", (nueva_especie, id_mascota))
        if nueva_edad:
            cursor.execute("UPDATE mascotas SET edad = %s WHERE id_mascota = %s", (nueva_edad, id_mascota))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Mascota actualizada")
    except:
        print("❌ Error")
    input("Presioná Enter...")

# ========== VETERINARIOS ==========
def menu_veterinarios():
    while True:
        print("\n" + "-" * 40)
        print("  👨‍⚕️ GESTIÓN DE VETERINARIOS")
        print("-" * 40)
        print("  1. Alta")
        print("  2. Baja")
        print("  3. Modificación")
        print("  4. Ver todos")
        print("  5. Volver")
        
        op = input("👉 Opción: ")
        
        if op == "1":
            alta_veterinario()
        elif op == "2":
            baja_veterinario()
        elif op == "3":
            modificar_veterinario()
        elif op == "4":
            ver_veterinarios()
        elif op == "5":
            break
        else:
            print("❌ Opción inválida")
            input("Presioná Enter...")

def alta_veterinario():
    print("\n--- NUEVO VETERINARIO ---")
    nombre = input("   Nombre: ")
    especialidad = input("   Especialidad: ")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO veterinarios (nombre, especialidad) VALUES (%s, %s)", (nombre, especialidad))
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Veterinario '{nombre}' agregado")
    input("Presioná Enter...")

def ver_veterinarios():
    print("\n--- LISTADO DE VETERINARIOS ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_veterinario, nombre, especialidad FROM veterinarios")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if datos:
        print(tabulate(datos, headers=["ID", "NOMBRE", "ESPECIALIDAD"], tablefmt="rounded_grid"))
    else:
        print("ℹ️ No hay veterinarios registrados")
    input("Presioná Enter...")

def baja_veterinario():
    ver_veterinarios()
    try:
        id_vet = int(input("\nID del veterinario a eliminar: "))
        confirmar = input(f"¿Eliminar veterinario ID {id_vet}? (s/n): ").lower()
        if confirmar == "s":
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM veterinarios WHERE id_veterinario = %s", (id_vet,))
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Veterinario eliminado")
        else:
            print("❌ Cancelado")
    except:
        print("❌ ID inválido")
    input("Presioná Enter...")

def modificar_veterinario():
    ver_veterinarios()
    try:
        id_vet = int(input("\nID del veterinario a modificar: "))
        nuevo_nombre = input("Nuevo nombre (Enter si no cambia): ")
        nueva_especialidad = input("Nueva especialidad (Enter si no cambia): ")
        
        conn = conectar()
        cursor = conn.cursor()
        if nuevo_nombre:
            cursor.execute("UPDATE veterinarios SET nombre = %s WHERE id_veterinario = %s", (nuevo_nombre, id_vet))
        if nueva_especialidad:
            cursor.execute("UPDATE veterinarios SET especialidad = %s WHERE id_veterinario = %s", (nueva_especialidad, id_vet))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Veterinario actualizado")
    except:
        print("❌ Error")
    input("Presioná Enter...")

# ========== TURNOS ==========
def menu_turnos():
    while True:
        print("\n" + "-" * 40)
        print("  📅 GESTIÓN DE TURNOS")
        print("-" * 40)
        print("  1. Alta")
        print("  2. Baja")
        print("  3. Modificación")
        print("  4. Ver todos")
        print("  5. Volver")
        
        op = input("👉 Opción: ")
        
        if op == "1":
            alta_turno()
        elif op == "2":
            baja_turno()
        elif op == "3":
            modificar_turno()
        elif op == "4":
            ver_turnos()
        elif op == "5":
            break
        else:
            print("❌ Opción inválida")
            input("Presioná Enter...")

def alta_turno():
    print("\n--- NUEVO TURNO ---")
    
    conn = conectar()
    cursor = conn.cursor()
    
    # Mostrar mascotas
    cursor.execute("SELECT id_mascota, nombre FROM mascotas")
    mascotas = cursor.fetchall()
    if not mascotas:
        print("⚠️ No hay mascotas registradas")
        cursor.close()
        conn.close()
        input("Presioná Enter...")
        return
    print("\nMascotas:")
    print(tabulate(mascotas, headers=["ID", "NOMBRE"], tablefmt="simple"))
    id_mascota = int(input("   ID mascota: "))
    
    # Mostrar veterinarios
    cursor.execute("SELECT id_veterinario, nombre FROM veterinarios")
    vets = cursor.fetchall()
    print("\nVeterinarios:")
    print(tabulate(vets, headers=["ID", "NOMBRE"], tablefmt="simple"))
    id_veterinario = int(input("   ID veterinario: "))
    
    fecha = input("   Fecha (YYYY-MM-DD): ")
    hora = input("   Hora (HH:MM:SS): ")
    motivo = input("   Motivo: ")
    
    cursor.execute("INSERT INTO turnos (id_mascota, id_veterinario, fecha, hora, motivo) VALUES (%s, %s, %s, %s, %s)",
                   (id_mascota, id_veterinario, fecha, hora, motivo))
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ Turno agendado")
    input("Presioná Enter...")

def ver_turnos():
    print("\n--- LISTADO DE TURNOS ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id_turno, m.nombre, v.nombre, t.fecha, t.hora, t.motivo
        FROM turnos t
        JOIN mascotas m ON t.id_mascota = m.id_mascota
        JOIN veterinarios v ON t.id_veterinario = v.id_veterinario
        ORDER BY t.fecha DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if datos:
        print(tabulate(datos, headers=["ID", "MASCOTA", "VETERINARIO", "FECHA", "HORA", "MOTIVO"], tablefmt="rounded_grid"))
    else:
        print("ℹ️ No hay turnos registrados")
    input("Presioná Enter...")

def baja_turno():
    ver_turnos()
    try:
        id_turno = int(input("\nID del turno a cancelar: "))
        confirmar = input(f"¿Cancelar turno ID {id_turno}? (s/n): ").lower()
        if confirmar == "s":
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM turnos WHERE id_turno = %s", (id_turno,))
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Turno cancelado")
        else:
            print("❌ Cancelado")
    except:
        print("❌ ID inválido")
    input("Presioná Enter...")

def modificar_turno():
    ver_turnos()
    try:
        id_turno = int(input("\nID del turno a modificar: "))
        nueva_fecha = input("Nueva fecha (YYYY-MM-DD) (Enter si no cambia): ")
        nueva_hora = input("Nueva hora (HH:MM:SS) (Enter si no cambia): ")
        nuevo_motivo = input("Nuevo motivo (Enter si no cambia): ")
        
        conn = conectar()
        cursor = conn.cursor()
        if nueva_fecha:
            cursor.execute("UPDATE turnos SET fecha = %s WHERE id_turno = %s", (nueva_fecha, id_turno))
        if nueva_hora:
            cursor.execute("UPDATE turnos SET hora = %s WHERE id_turno = %s", (nueva_hora, id_turno))
        if nuevo_motivo:
            cursor.execute("UPDATE turnos SET motivo = %s WHERE id_turno = %s", (nuevo_motivo, id_turno))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Turno actualizado")
    except:
        print("❌ Error")
    input("Presioná Enter...")

# ========== EJECUTAR ==========
if __name__ == "__main__":
    menu()