"""
Tests for DELETE operations — DELETE /pet/{petId}
"""
import pytest

from clients import PetClient
from models import Pet, PetFactory
from utils import assert_status


@pytest.mark.delete
@pytest.mark.smoke
class TestDeletePet:

    def test_delete_pet_returns_200(self, client: PetClient):
        """DELETE /pet/{petId} for an existing pet should return HTTP 200."""
        # Create a dedicated pet for this test (not using created_pet fixture
        # since we want to control deletion ourselves here)
        pet = PetFactory.build()
        create_response = client.add_pet(pet)
        assert_status(create_response, 200)
        pet_id = create_response.json()["id"]

        delete_response = client.delete_pet(pet_id)
        assert_status(delete_response, 200)

    def test_deleted_pet_is_not_retrievable(self, client: PetClient):
        """After deletion, GET /pet/{petId} should return HTTP 404."""
        pet = PetFactory.build()
        create_response = client.add_pet(pet)
        assert_status(create_response, 200)
        pet_id = create_response.json()["id"]

        client.delete_pet(pet_id)

        get_response = client.get_pet_by_id(pet_id)
        assert_status(get_response, 404)

    def test_delete_is_idempotent(self, client: PetClient):
        """Deleting an already-deleted pet should return 404, not a server error."""
        pet = PetFactory.build()
        create_response = client.add_pet(pet)
        assert_status(create_response, 200)
        pet_id = create_response.json()["id"]

        # First deletion
        first = client.delete_pet(pet_id)
        assert_status(first, 200)

        # Second deletion of same ID
        second = client.delete_pet(pet_id)
        assert second.status_code == 404, (
            f"Second delete of same pet should return 404, got {second.status_code}"
        )

    @pytest.mark.negative
    def test_delete_nonexistent_pet_returns_404(self, client: PetClient):
        """DELETE /pet/{petId} for a non-existent ID must return HTTP 404."""
        response = client.delete_pet(999_999_996)
        assert_status(response, 404)

    @pytest.mark.negative
    def test_delete_pet_with_invalid_id_returns_400(self, client: PetClient):
        """DELETE /pet/{petId} with a non-integer ID should return HTTP 400."""
        import requests
        from config import config
        raw = requests.delete(f"{config.BASE_URL}/pet/not-a-number", timeout=10)
        assert raw.status_code == 400, (
            f"Expected 400 for invalid pet ID format, got {raw.status_code}"
        )
