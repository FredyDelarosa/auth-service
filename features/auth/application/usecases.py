from features.auth.domain.ports import UserRepository
from features.auth.domain.entities import Usuario
from features.auth.application.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from core.security.hashing import verify_password, get_password_hash
from core.security.jwt_manager import create_access_token
import uuid

class AuthUseCases:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def login(self, req: LoginRequest) -> TokenResponse:
        user = self.repo.get_by_email(req.email)
        if not user or not verify_password(req.password, user.password_hash):
            raise ValueError("Credenciales inválidas")
        if not user.esta_activo:
            raise ValueError("Usuario inactivo")

        roles_list = [r.nombre_rol for r in user.roles]
        token = create_access_token(data={"sub": user.id_usuario, "roles": roles_list})
        return TokenResponse(access_token=token)

    def register(self, req: RegisterRequest) -> UserResponse:
        if self.repo.get_by_email(req.email):
            raise ValueError("El email ya está registrado")
            
        from features.auth.domain.entities import Rol
        nuevo_usuario = Usuario(
            id_usuario=str(uuid.uuid4()),
            nombre=req.nombre,
            email=req.email,
            password_hash=get_password_hash(req.password),
            roles=[Rol(id_rol="", nombre_rol=req.rol)]
        )
        user_db = self.repo.create(nuevo_usuario)
        return UserResponse(
            id_usuario=user_db.id_usuario,
            nombre=user_db.nombre,
            email=user_db.email,
            roles=[r.nombre_rol for r in user_db.roles]
        )

    def get_user_info(self, id_usuario: str) -> UserResponse:
        user = self.repo.get_by_id(id_usuario)
        if not user:
            raise ValueError("Usuario no encontrado")
        return UserResponse(
            id_usuario=user.id_usuario,
            nombre=user.nombre,
            email=user.email,
            roles=[r.nombre_rol for r in user.roles]
        )

    def get_all_users(self, rol: str = None) -> list[UserResponse]:
        users = self.repo.get_all(rol)
        return [
            UserResponse(
                id_usuario=u.id_usuario,
                nombre=u.nombre,
                email=u.email,
                roles=[r.nombre_rol for r in u.roles]
            ) for u in users
        ]
