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
