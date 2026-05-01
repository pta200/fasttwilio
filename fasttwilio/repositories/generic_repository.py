import uuid
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

# Generic type variable for domain entities
T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[T]:
        """Get an existing entity by id"""
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: T) -> Optional[T]:
        """Add entity"""
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, offset: int, limit: int) -> List[T]:
        """Paginate over entities"""
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: uuid.UUID, entity: T) -> Optional[T]:
        """Update an existing entity"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> bool:
        """Remove an entity by its identifier"""
        raise NotImplementedError
