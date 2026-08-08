from typing import Annotated

from fastapi import Depends

from src.domain.identity.use_cases.get_user import GerCurrentUserUseCase
from src.domain.identity.use_cases.login import LoginUseCase
from src.domain.identity.use_cases.logout import LogOutUseCase
from src.domain.identity.use_cases.refresh import RefreshTokenUseCase
from src.presentation.api.dependencies import (
    get_payload,
    get_user_di,
    login_di,
    logout_di,
    refresh_di,
)

GetCurrentUserDepends = Annotated[GerCurrentUserUseCase, Depends(get_user_di)]
PayloadDepends = Annotated[dict, Depends(get_payload)]
LoginDepends = Annotated[LoginUseCase, Depends(login_di)]
RefreshDepends = Annotated[RefreshTokenUseCase, Depends(refresh_di)]
LogOutDepends = Annotated[LogOutUseCase, Depends(logout_di)]