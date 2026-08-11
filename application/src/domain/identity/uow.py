from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.identity.repository import ProfileRepository
from src.infrastructure.database.uow import BaseUnitOfWork


class ProfileUnitOfWork(BaseUnitOfWork):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        super().__init__(session)
        self._profile: ProfileRepository | None = None

    @property
    def profile(self) -> ProfileRepository:
        if self._profile is None:
            self._profile = ProfileRepository(self.session)
            return self._profile
        return self._profile
