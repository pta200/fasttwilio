import uuid
from fastapi.testclient import TestClient
from datetime import datetime, timezone
import pytest
import urllib.parse


@pytest.mark.asyncio
async def test_add_student(client: TestClient):
    data = {
        "course": "Experiments, Science, and Fashion in Nanophotonics",
        "email": "jdoe@example.com",
        "gpa": 3,
        "mobile": "+12125555555",
        "name": "Jane Doe"
    }

    response = client.post(
        "/students", json=data
    )
    assert response.status_code == 201