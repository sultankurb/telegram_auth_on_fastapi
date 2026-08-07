from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.base_repo import SQLAlchemyRepository
from src.infrastructure.database.models import Profile


class ProfileRepository(SQLAlchemyRepository[Profile]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=Profile)

    async def find_by_id(self, id: int) -> Profile | None:
        profile = await self._get_by_filter(field=Profile.id, value=id)
        return profile

    async def exist(self, id: int) -> bool:
        result = await self._exists(field=Profile.id, value=id)
        return result

    async def create(self, profile: Profile) -> Profile:
        pass

    async def update(self, profile: Profile) -> Profile:
        pass
