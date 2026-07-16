import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

# URLs de conexión. 
# La base de datos vieja (Core/Monolito)
DB_URL_CORE = os.getenv("DATABASE_URL") 
# La nueva base de datos exclusiva para Auth
DB_URL_AUTH = os.getenv("DB_URL_AUTH")

def migrar_usuarios():
    print("Iniciando migración de usuarios...")
    
    if not DB_URL_CORE or not DB_URL_AUTH:
        print("Error: Asegúrate de tener DATABASE_URL y DB_URL_AUTH en tu .env global")
        return

    engine_core = create_engine(DB_URL_CORE)
    engine_auth = create_engine(DB_URL_AUTH)

    with engine_core.connect() as conn_core, engine_auth.connect() as conn_auth:
        # 1. Extraer roles del sistema viejo
        print("Migrando roles...")
        roles = conn_core.execute(text("SELECT id_rol, nombre_rol FROM roles")).fetchall()
        for rol in roles:
            # Insertar ignorando duplicados (ON CONFLICT DO NOTHING funciona en Postgres)
            conn_auth.execute(text("""
                INSERT INTO roles (id_rol, nombre_rol) 
                VALUES (:id_rol, :nombre_rol) 
                ON CONFLICT (id_rol) DO NOTHING
            """), {"id_rol": rol.id_rol, "nombre_rol": rol.nombre_rol})
        
        # 2. Extraer usuarios del sistema viejo
        print("Migrando usuarios...")
        usuarios = conn_core.execute(text("SELECT id_usuario, nombre, email, password_hash, esta_activo FROM usuarios")).fetchall()
        for u in usuarios:
            conn_auth.execute(text("""
                INSERT INTO usuarios (id_usuario, nombre, email, password_hash, esta_activo)
                VALUES (:id_usuario, :nombre, :email, :password_hash, :esta_activo)
                ON CONFLICT (id_usuario) DO NOTHING
            """), {
                "id_usuario": u.id_usuario,
                "nombre": u.nombre,
                "email": u.email,
                "password_hash": u.password_hash,
                "esta_activo": u.esta_activo
            })
            
        # 3. Extraer relación usuario_rol
        print("Migrando relaciones usuario_rol...")
        user_roles = conn_core.execute(text("SELECT usuario_id, rol_id FROM usuario_rol")).fetchall()
        for ur in user_roles:
            try:
                conn_auth.execute(text("""
                    INSERT INTO usuario_rol (usuario_id, rol_id)
                    VALUES (:usuario_id, :rol_id)
                """), {"usuario_id": ur.usuario_id, "rol_id": ur.rol_id})
            except Exception:
                # Si ya existe, lo ignoramos
                pass
                
        conn_auth.commit()
        print("¡Migración completada con éxito!")

if __name__ == "__main__":
    migrar_usuarios()
