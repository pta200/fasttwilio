import uuid
from fastapi.testclient import TestClient
from datetime import datetime, timezone
import pytest
import json


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

@pytest.mark.asyncio
async def test_get_all_students(client: TestClient):
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data.get("students")) == 1

@pytest.mark.asyncio
async def test_get_student(client: TestClient):
    payload = {
        "course": "Experiments, Science, and Fashion in Nanophotonics",
        "email": "fs@example.com",
        "gpa": 3,
        "mobile": "+12125555555",
        "name": "Fred Sanford"
    }

    response = client.post(
        "/students", json=payload
    )
    assert response.status_code == 201
    student = response.json()

    response = client.get(f"/students/{student.get("student_id")}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data.get("student_id") == student.get("student_id")


