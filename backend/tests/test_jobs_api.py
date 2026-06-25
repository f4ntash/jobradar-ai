from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_job_with_default_status():
    response = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Backend Developer"
    assert data["status"] == "saved"


def test_create_job_accepts_valid_non_default_status():
    response = client.post(
        "/jobs",
        json={
            "title": "Backend Developer",
            "url": "https://example.com/job-1",
            "status": "interview",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "interview"


def test_create_job_rejects_invalid_status():
    response = client.post(
        "/jobs",
        json={
            "title": "Backend Developer",
            "url": "https://example.com/job-1",
            "status": "pending",
        },
    )

    assert response.status_code == 422
    assert "Invalid status 'pending'." in response.json()["detail"]


def test_list_jobs_returns_empty_list():
    response = client.get("/jobs")

    assert response.status_code == 200
    assert response.json() == []


def test_list_jobs_after_creating_jobs():
    client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    )
    client.post(
        "/jobs",
        json={"title": "Python Developer", "url": "https://example.com/job-2"},
    )

    response = client.get("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Backend Developer"
    assert data[1]["title"] == "Python Developer"


def test_create_job_rejects_duplicate_url():
    payload = {"title": "Backend Developer", "url": "https://example.com/job-1"}

    assert client.post("/jobs", json=payload).status_code == 201
    response = client.post("/jobs", json=payload)

    assert response.status_code == 400


def test_get_job_by_id_returns_job():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    response = client.get(f"/jobs/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_job_by_id_returns_404_when_missing():
    response = client.get("/jobs/999")

    assert response.status_code == 404


def test_patch_job_updates_status():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    response = client.patch(f"/jobs/{created['id']}", json={"status": "applied"})

    assert response.status_code == 200
    assert response.json()["status"] == "applied"


def test_patch_job_rejects_invalid_status():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    response = client.patch(f"/jobs/{created['id']}", json={"status": "pending"})

    assert response.status_code == 422
    assert "Invalid status 'pending'." in response.json()["detail"]
    assert "saved" in response.json()["detail"]


def test_patch_job_rejects_null_status():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    response = client.patch(f"/jobs/{created['id']}", json={"status": None})

    assert response.status_code == 422


def test_patch_missing_job_returns_404():
    response = client.patch("/jobs/999", json={"title": "Updated title"})

    assert response.status_code == 404


def test_delete_job_success():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    delete_response = client.delete(f"/jobs/{created['id']}")
    get_response = client.get(f"/jobs/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_missing_job_returns_404():
    response = client.delete("/jobs/999")

    assert response.status_code == 404


def test_patch_job_rejects_duplicate_url():
    first = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()
    second = client.post(
        "/jobs",
        json={"title": "Python Developer", "url": "https://example.com/job-2"},
    ).json()

    response = client.patch(
        f"/jobs/{second['id']}",
        json={"url": first["url"]},
    )

    assert response.status_code == 400
