import uuid
from sqlalchemy import Column, String, Boolean, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.db.connection import Base

usuario_rol_table = Table(
    'usuario_rol', Base.metadata,
    Column('usuario_id', UUID(as_uuid=True), ForeignKey('usuarios.id_usuario')),
    Column('rol_id', UUID(as_uuid=True), ForeignKey('roles.id_rol'))
)

class RolModel(Base):
    __tablename__ = 'roles'
    id_rol = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_rol = Column(String(50), unique=True, nullable=False)

class UsuarioModel(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    esta_activo = Column(Boolean, default=True)
    
    roles = relationship("RolModel", secondary=usuario_rol_table)
