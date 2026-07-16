from typing import List, Optional

class Rol:
    def __init__(self, id_rol: str, nombre_rol: str):
        self.id_rol = id_rol
        self.nombre_rol = nombre_rol

class Usuario:
    def __init__(
        self,
        id_usuario: str,
        nombre: str,
        email: str,
        password_hash: str,
        roles: Optional[List[Rol]] = None,
        esta_activo: bool = True
    ):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.roles = roles or []
        self.esta_activo = esta_activo
