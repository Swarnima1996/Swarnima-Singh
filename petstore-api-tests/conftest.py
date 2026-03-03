"""
conftest.py — pytest fixtures shared across the entire test suite.

Fixtures here are auto-available to all test files without explicit imports.
"""
import pytest

from clients import PetClient
from models import Pet, PetFactory


@pytest.fixture(scope="session")
def client() -> PetClient:
    """
    Session-scoped PetClient.
    One HTTP session is reused across all tests for efficiency.
    """
    return PetClient()


@pytest.fixture(scope="function")
def created_pet(client: PetClient) -> Pet:
    """
    Function-scoped fixture that creates a pet before the test
    and deletes it afterwards (teardown), ensuring test isolation.
    """
    pet = PetFactory.build(status="available")
    response = client.add_pet(pet)
    assert response.status_code == 200, (
        f"Setup failed: could not create pet. Response: {response.text}"
    )
    created = response.json()
    pet.id = created["id"]

    yield pet  # hand the pet to the test

    # --- teardown ---
    client.delete_pet(pet.id)


@pytest.fixture(scope="function")
def pet_payload() -> Pet:
    """Return a freshly generated Pet instance (not yet created via API)."""
    return PetFactory.build()


@pytest.fixture(scope="function")
def tracked_client(client: PetClient):
    """
    Fixture for tests that create pets directly (e.g. TestCreatePet).

    Yields a (client, created_ids) tuple. Tests append any created pet ID
    to created_ids and all pets are deleted in teardown, ensuring no
    orphaned data is left in the API regardless of test outcome.

    Usage:
        def test_something(self, tracked_client):
            client, created_ids = tracked_client
            response = client.add_pet(pet)
            created_ids.append(response.json()["id"])
    """
    created_ids: list[int] = []
    yield client, created_ids

    # --- teardown: clean up every pet registered during the test ---
    for pet_id in created_ids:
        client.delete_pet(pet_id)