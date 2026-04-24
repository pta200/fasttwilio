import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_add_student(client: TestClient, token: str):
    data = {
        "course": "Experiments, Science, and Fashion in Nanophotonics",
        "email": "jdoe@example.com",
        "gpa": 3,
        "mobile": "+12125555555",
        "name": "Jane Doe",
    }

    response = client.post(
        "/students", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_all_students(client: TestClient, token: str):
    response = client.get("/students", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("students")) == 1


@pytest.mark.asyncio
async def test_get_student(client: TestClient, token: str):
    payload = {
        "course": "Experiments, Science, and Fashion in Nanophotonics",
        "email": "fs@example.com",
        "gpa": 3,
        "mobile": "+12125555555",
        "name": "Fred Sanford",
    }

    response = client.post(
        "/students", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    student = response.json()

    response = client.get(
        f"/students/{student.get("student_id")}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("student_id") == student.get("student_id")


@pytest.mark.asyncio
async def test_update_student(client: TestClient, token: str):
    response = client.get("/students", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    students = response.json().get("students")

    payload = {"course": "Computer Science and Math", "gpa": 3.5}

    response = client.put(
        f"/students/{students[0].get('student_id')}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("course") == payload.get("course")


@pytest.mark.asyncio
async def test_delete_student(client: TestClient, token: str):
    response = client.get("/students", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    students = response.json().get("students")

    response = client.delete(
        f"/students/{students[0].get('student_id')}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204
