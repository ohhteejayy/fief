import dataclasses
from collections.abc import Callable
from typing import AsyncContextManager

import httpx
from fastapi import FastAPI

from fief.db.types import DatabaseConnectionParameters, DatabaseType
from fief.models import (
    Client,
    LoginSession,
    RegistrationSession,
    SessionToken,
    Tenant,
    User,
)


@dataclasses.dataclass
class TenantParams:
    path_prefix: str
    tenant: Tenant
    client: Client
    user: User
    login_session: LoginSession
    registration_session_password: RegistrationSession
    registration_session_oauth: RegistrationSession
    session_token: SessionToken
    session_token_token: tuple[str, str]


HTTPClientGeneratorType = Callable[[FastAPI], AsyncContextManager[httpx.AsyncClient]]

GetTestDatabase = Callable[
    ..., AsyncContextManager[tuple[DatabaseConnectionParameters, DatabaseType]]
]
