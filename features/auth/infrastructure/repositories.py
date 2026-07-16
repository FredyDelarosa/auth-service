from typing import Optional
from sqlalchemy.orm import Session
from features.auth.domain.ports import UserRepository
from features.auth.domain.entities import Usuario, Rol
from .models import UsuarioModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: UsuarioModel) -> Usuario:
        roles = [Rol(id_rol=str(r.id_rol), nombre_rol=r.nombre_rol) for r in model.roles]
        return Usuario(
            id_usuario=str(model.id_usuario),
            nombre=model.nombre,
            email=model.email,
            password_hash=model.password_hash,
            roles=roles,
            esta_activo=model.esta_activo
        )

    def get_by_email(self, email: str) -> Optional[Usuario]:
        model = self.db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        return self._to_entity(model) if model else None

    def get_by_id(self, id_usuario: str) -> Optional[Usuario]:
        model = self.db.query(UsuarioModel).filter(UsuarioModel.id_usuario == id_usuario).first()
        return self._to_entity(model) if model else None

    def create(self, usuario: Usuario) -> Usuario:
        # En una implementación real, se manejan los roles adecuadamente.
        nuevo_modelo = UsuarioModel(
            nombre=usuario.nombre,
            email=usuario.email,
            password_hash=usuario.password_hash
        )
        self.db.add(nuevo_modelo)
        self.db.commit()
        self.db.refresh(nuevo_modelo)
        return self._to_entity(nuevo_modelo)
