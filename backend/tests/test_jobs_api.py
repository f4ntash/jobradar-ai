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


def test_create_job():
    response = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Backend Developer"
    assert data["status"] == "saved"


def test_reject_duplicate_url():
    payload = {"title": "Backend Developer", "url": "https://example.com/job-1"}

    assert client.post("/jobs", json=payload).status_code == 201
    response = client.post("/jobs", json=payload)

    assert response.status_code == 400


def test_get_job_by_id():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    response = client.get(f"/jobs/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_update_status():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    response = client.patch(f"/jobs/{created['id']}", json={"status": "applied"})

    assert response.status_code == 200
    assert response.json()["status"] == "applied"


def test_reject_invalid_status():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    response = client.patch(f"/jobs/{created['id']}", json={"status": "pending"})

    assert response.status_code == 422


def test_reject_null_status_update():
    created = client.post(
        "/jobs",
        json={"title": "Backend Developer", "url": "https://example.com/job-1"},
    ).json()

    response = client.patch(f"/jobs/{created['id']}", json={"status": None})

    assert response.status_code == 422
