"""
Tests for READ operations — GET /pet/{petId}, GET /pet/findByStatus, GET /pet/findByTags
"""
import pytest

from clients import PetClient
from models import Pet, PetFactory
from utils import assert_status, assert_pet_schema, assert_pet_matches


@pytest.mark.read
@pytest.mark.smoke
class TestReadPetById:

    def test_get_pet_by_id_returns_200(self, client: PetClient, created_pet: Pet):
        """GET /pet/{petId} for an existing pet should return HTTP 200."""
        response = client.get_pet_by_id(created_pet.id)
        assert_status(response, 200)

    def test_get_pet_by_id_returns_correct_pet(self, client: PetClient, created_pet: Pet):
        """The returned pet must match the pet that was created."""
        response = client.get_pet_by_id(created_pet.id)
        assert_status(response, 200)
        body = response.json()
        assert_pet_matches(body, id=created_pet.id, name=created_pet.name)

    def test_get_pet_by_id_has_required_fields(self, client: PetClient, created_pet: Pet):
        """Response body must contain all required fields defined by the schema."""
        response = client.get_pet_by_id(created_pet.id)
        assert_status(response, 200)
        assert_pet_schema(response.json())

    @pytest.mark.negative
    def test_get_pet_by_nonexistent_id_returns_404(self, client: PetClient):
        """GET /pet/{petId} for a non-existent ID must return HTTP 404."""
        response = client.get_pet_by_id(999_999_999)
        assert_status(response, 404)

    @pytest.mark.negative
    def test_get_pet_by_invalid_id_returns_400(self, client: PetClient):
        """GET /pet/{petId} with a non-integer ID should return HTTP 400."""
        import requests
        from config import config
        raw = requests.get(f"{config.BASE_URL}/pet/not-an-id", timeout=10)
        assert raw.status_code == 400, (
            f"Expected 400 for invalid ID type, got {raw.status_code}"
        )


@pytest.mark.read
class TestFindPetsByStatus:

    def test_find_by_status_available_returns_200(self, client: PetClient):
        """GET /pet/findByStatus?status=available should return HTTP 200."""
        response = client.find_pets_by_status("available")
        assert_status(response, 200)

    def test_find_by_status_returns_list(self, client: PetClient):
        """findByStatus should return a JSON array."""
        response = client.find_pets_by_status("available")
        assert_status(response, 200)
        body = response.json()
        assert isinstance(body, list), f"Expected a list, got {type(body)}"

    def test_find_by_status_results_match_requested_status(self, client: PetClient):
        """Every pet in the response must have the requested status."""
        for status in ("available", "pending", "sold"):
            response = client.find_pets_by_status(status)
            assert_status(response, 200)
            pets = response.json()
            for pet in pets:
                assert pet.get("status") == status, (
                    f"Pet {pet.get('id')} has status '{pet.get('status')}', expected '{status}'"
                )

    def test_find_by_status_each_item_has_required_fields(self, client: PetClient):
        """Each pet in the findByStatus response must have required Pet fields."""
        response = client.find_pets_by_status("available")
        assert_status(response, 200)
        for pet in response.json()[:5]:  # check first 5 to avoid long loops
            assert_pet_schema(pet)

    @pytest.mark.negative
    def test_find_by_invalid_status_returns_400(self, client: PetClient):
        """findByStatus with an invalid status value should return HTTP 400."""
        response = client.find_pets_by_status("nonexistent-status")
        assert_status(response, 400)


@pytest.mark.read
class TestFindPetsByTags:

    def test_find_by_tags_returns_200(self, client: PetClient):
        """GET /pet/findByTags with a valid tag should return HTTP 200."""
        response = client.find_pets_by_tags(["tag1"])
        assert_status(response, 200)

    def test_find_by_tags_returns_list(self, client: PetClient):
        """findByTags should return a JSON array."""
        response = client.find_pets_by_tags(["tag1"])
        assert_status(response, 200)
        assert isinstance(response.json(), list)

    def test_find_by_multiple_tags_returns_200(self, client: PetClient):
        """findByTags should accept multiple tags in a single request."""
        response = client.find_pets_by_tags(["tag1", "tag2", "tag3"])
        assert_status(response, 200)
