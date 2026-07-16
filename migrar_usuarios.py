import os
import uuid
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

DB_URL_CORE = os.getenv("DATABASE_URL")
DB_URL_AUTH = os.getenv("DB_URL_AUTH")

def migrar_usuarios():
    print("Iniciando migración de usuarios...")
    if not DB_URL_CORE or not DB_URL_AUTH:
        print("Error: Asegúrate de tener DATABASE_URL y DB_URL_AUTH.")
        return

    engine_core = create_engine(DB_URL_CORE)
    engine_auth = create_engine(DB_URL_AUTH)

    with engine_core.connect() as conn_core, engine_auth.connect() as conn_auth:
        # 1. Obtener todos los usuarios del sistema viejo (donde 'rol' es un string)
        print("Extrayendo usuarios antiguos...")
        usuarios = conn_core.execute(text("SELECT id_usuario, nombre, email, password_hash, rol, activo FROM usuarios")).fetchall()
        
        # 2. Crear los roles únicos en la nueva base de datos Auth
        roles_unicos = set(u.rol for u in usuarios if u.rol)
        role_map = {}
        print(f"Roles encontrados para migrar: {roles_unicos}")
        
        for rol_nombre in roles_unicos:
            # Buscar si el rol ya existe
            rol_existente = conn_auth.execute(text("SELECT id_rol FROM roles WHERE nombre_rol = :nombre"), {"nombre": rol_nombre}).fetchone()
            if rol_existente:
                role_map[rol_nombre] = rol_existente.id_rol
            else:
                nuevo_id = str(uuid.uuid4())
                conn_auth.execute(text("INSERT INTO roles (id_rol, nombre_rol) VALUES (:id, :nombre)"), {"id": nuevo_id, "nombre": rol_nombre})
                role_map[rol_nombre] = nuevo_id
                
        # 3. Insertar usuarios y sus relaciones de rol en la nueva BD Auth
        print("Migrando usuarios y mapeando roles...")
        for u in usuarios:
            # Insertar en usuarios
            conn_auth.execute(text("""
                INSERT INTO usuarios (id_usuario, nombre, email, password_hash, esta_activo)
                VALUES (:id, :nom, :em, :pwd, :act)
                ON CONFLICT (id_usuario) DO NOTHING
            """), {
                "id": u.id_usuario,
                "nom": u.nombre,
                "em": u.email,
                "pwd": u.password_hash,
                "act": u.activo
            })
            
            # Insertar en usuario_rol
            if u.rol and u.rol in role_map:
                try:
                    conn_auth.execute(text("""
                        INSERT INTO usuario_rol (usuario_id, rol_id)
                        VALUES (:u_id, :r_id)
                    """), {"u_id": u.id_usuario, "r_id": role_map[u.rol]})
                except Exception:
                    pass # Ya existe la relacion
                    
        conn_auth.commit()
        print("¡Migración completada con éxito!")

if __name__ == "__main__":
    migrar_usuarios()
