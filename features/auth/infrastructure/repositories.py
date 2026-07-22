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
        from .models import RolModel
        
        nuevo_modelo = UsuarioModel(
            nombre=usuario.nombre,
            email=usuario.email,
            password_hash=usuario.password_hash
        )
        
        # Asignar roles
        if usuario.roles:
            for rol in usuario.roles:
                rol_db = self.db.query(RolModel).filter(RolModel.nombre_rol == rol.nombre_rol).first()
                if not rol_db:
                    rol_db = RolModel(nombre_rol=rol.nombre_rol)
                    self.db.add(rol_db)
                nuevo_modelo.roles.append(rol_db)
                
        self.db.add(nuevo_modelo)
        self.db.commit()
        self.db.refresh(nuevo_modelo)
        return self._to_entity(nuevo_modelo)

    def get_all(self, rol: Optional[str] = None) -> list[Usuario]:
        query = self.db.query(UsuarioModel)
        if rol:
            from .models import RolModel
            query = query.join(UsuarioModel.roles).filter(RolModel.nombre_rol == rol)
        models = query.all()
        return [self._to_entity(m) for m in models]

    def update_role(self, id_usuario: str, rol: str) -> Optional[Usuario]:
        from .models import RolModel
        model = self.db.query(UsuarioModel).filter(UsuarioModel.id_usuario == id_usuario).first()
        if not model:
            return None
        
        rol_db = self.db.query(RolModel).filter(RolModel.nombre_rol == rol).first()
        if not rol_db:
            rol_db = RolModel(nombre_rol=rol)
            self.db.add(rol_db)
            
        model.roles = [rol_db] # Sobrescribe los roles anteriores con el nuevo
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def delete(self, id_usuario: str) -> bool:
        model = self.db.query(UsuarioModel).filter(UsuarioModel.id_usuario == id_usuario).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True
