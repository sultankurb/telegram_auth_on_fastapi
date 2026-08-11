from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.base_repo import SQLAlchemyRepository
from src.infrastructure.database.models import Profile


class ProfileRepository(SQLAlchemyRepository[Profile]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=Profile)

    async def find_by_id(self, id: int) -> Profile | None:
        profile = await self._get_by_filter(self._model_cls.id == id)
        return profile

    async def exist(self, telegram_id: int) -> bool:
        result = await self._exists(self._model_cls.telegram_id == telegram_id)
        return result

    async def upsert_telegram_user(
        self,
        user_data: dict[str, Any],
    ) -> Profile:
        stmt = insert(self._model_cls).values(
            telegram_id=user_data["id"],
            first_name=user_data["first_name"],
            username=user_data["username"],
            photo_url=user_data["photo_url"],
            last_name=user_data["last_name"]
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[self._model_cls.telegram_id],
            set_={
                "first_name": stmt.excluded.first_name,
                "username": stmt.excluded.username,
                "photo_url": stmt.excluded.photo_url,
                "last_name": stmt.excluded.last_name
            },
        ).returning(self._model_cls)

        result = await self._session.execute(stmt)
        return result.scalar_one()
