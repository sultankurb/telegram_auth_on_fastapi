from collections.abc import Mapping
from typing import Any, TypeVar

from sqlalchemy import Executable, delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

OrmModel = TypeVar("OrmModel")


class SQLAlchemyRepository[OrmModel]:
    def __init__(self, session: AsyncSession, model_cls: type[OrmModel]):
        self._session = session
        self._model_cls = model_cls

    async def _scalar_one_or_none(self, stmt: Executable) -> OrmModel | None:
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def _add(self, obj: OrmModel) -> OrmModel:
        self._session.add(obj)
        await self._session.flush()
        return obj

    async def _get_by_filter(
        self,
        *conditions,
    ) -> OrmModel | None:
        stmt = select(self._model_cls).where(*conditions)
        orm_obj = await self._scalar_one_or_none(stmt)
        return orm_obj

    async def _get_by_id(self, id: int) -> OrmModel | None:
        return await self._session.get(self._model_cls, id)

    async def _update(
        self, *conditions, data: Mapping[str, Any]
    ) -> OrmModel | None:
        stmt = (
            update(self._model_cls)
            .where(*conditions)
            .values(**data)
            .returning(self._model_cls)
        )
        result = await self._scalar_one_or_none(stmt)
        return result

    async def _delete_by_id(self, *conditions) -> bool:
        stmt = (
            delete(self._model_cls)
            .where(*conditions)
            .returning(self._model_cls)
        )
        deleted = await self._scalar_one_or_none(stmt)
        await self._session.flush()
        return deleted is not None

    async def _exists(
        self,
        *conditions,
    ) -> bool:
        stmt = select(exists().where(*conditions))
        result = await self._session.execute(stmt)
        return bool(result.scalar())
