import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Ver tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("[*] Tablas en users.db:", tables)

for table_name in tables:
    t = table_name[0]
    print(f"\n[*] Contenido de la tabla '{t}':")
    cursor.execute(f"SELECT * FROM {t}")
    rows = cursor.fetchall()
    
    # Obtener nombres de columnas
    cursor.execute(f"PRAGMA table_info({t})")
    cols = [col[1] for col in cursor.fetchall()]
    print("Columnas:", cols)
    for r in rows:
        print(" ", r)

conn.close()
