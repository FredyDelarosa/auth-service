from abc import ABC, abstractmethod
from typing import Optional
from .entities import Usuario

class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def get_by_id(self, id_usuario: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def create(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def get_all(self, rol: Optional[str] = None) -> list[Usuario]:
        pass
