import httpx
import pytest
from fastapi import status

from tests.data import TestData


@pytest.mark.asyncio
class TestListTenants:
    async def test_unauthorized(self, test_client_admin: httpx.AsyncClient):
        response = await test_client_admin.get("/tenants/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.admin_session_token(user="regular")
    async def test_valid(
        self, test_client_admin: httpx.AsyncClient, test_data: TestData
    ):
        response = await test_client_admin.get("/tenants/")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["count"] == len(test_data["tenants"])
