"""
Tests for UPDATE operations — PUT /pet, POST /pet/{petId}
"""
import pytest

from clients import PetClient
from models import Pet, PetFactory
from utils import assert_status, assert_pet_schema, assert_pet_matches


@pytest.mark.update
@pytest.mark.smoke
class TestUpdatePetFull:
    """Tests for PUT /pet — full resource update."""

    def test_update_pet_name_returns_200(self, client: PetClient, created_pet: Pet):
        """PUT /pet with updated name should return HTTP 200."""
        created_pet.name = "UpdatedPetName"
        response = client.update_pet(created_pet)
        assert_status(response, 200)

    def test_update_pet_name_is_persisted(self, client: PetClient, created_pet: Pet):
        """Updated name must be reflected when the pet is fetched by ID."""
        created_pet.name = "PersistenceCheck"
        client.update_pet(created_pet)

        fetched = client.get_pet_by_id(created_pet.id)
        assert_status(fetched, 200)
        assert_pet_matches(fetched.json(), name="PersistenceCheck")

    def test_update_pet_status_is_persisted(self, client: PetClient, created_pet: Pet):
        """Updated status must be reflected when the pet is fetched by ID."""
        created_pet.status = "sold"
        client.update_pet(created_pet)

        fetched = client.get_pet_by_id(created_pet.id)
        assert_status(fetched, 200)
        assert_pet_matches(fetched.json(), status="sold")

    def test_update_pet_response_has_required_fields(self, client: PetClient, created_pet: Pet):
        """PUT /pet response body must contain all required Pet fields."""
        created_pet.name = "FieldCheckPet"
        response = client.update_pet(created_pet)
        assert_status(response, 200)
        assert_pet_schema(response.json())

    def test_update_pet_preserves_id(self, client: PetClient, created_pet: Pet):
        """The pet ID must remain unchanged after an update."""
        original_id = created_pet.id
        created_pet.name = "IdPreservationTest"
        response = client.update_pet(created_pet)
        assert_status(response, 200)
        assert_pet_matches(response.json(), id=original_id)

    def test_update_pet_all_status_transitions(self, client: PetClient, created_pet: Pet):
        """A pet's status should be updatable to each valid value."""
        for status in ("pending", "sold", "available"):
            created_pet.status = status
            response = client.update_pet(created_pet)
            assert_status(response, 200)
            assert_pet_matches(response.json(), status=status)

    @pytest.mark.negative
    def test_update_nonexistent_pet_returns_error(self, client: PetClient):
        """PUT /pet for a pet ID that does not exist should return a 4xx error."""
        ghost_pet = PetFactory.build(pet_id=999_999_998)
        response = client.update_pet(ghost_pet)
        assert response.status_code in (404, 405), (
            f"Expected 404 or 405 for non-existent pet update, got {response.status_code}"
        )


@pytest.mark.update
class TestUpdatePetWithForm:
    """Tests for POST /pet/{petId} — partial update via form params."""

    def test_form_update_name_returns_200(self, client: PetClient, created_pet: Pet):
        """POST /pet/{petId} with new name should return HTTP 200."""
        response = client.update_pet_with_form(
            pet_id=created_pet.id,
            name="FormUpdatedName",
            status=created_pet.status,
        )
        assert_status(response, 200)

    def test_form_update_name_is_persisted(self, client: PetClient, created_pet: Pet):
        """Name updated via form POST must be reflected on subsequent GET."""
        client.update_pet_with_form(
            pet_id=created_pet.id,
            name="FormPersistName",
            status="available",
        )
        fetched = client.get_pet_by_id(created_pet.id)
        assert_status(fetched, 200)
        assert_pet_matches(fetched.json(), name="FormPersistName")

    @pytest.mark.negative
    def test_form_update_nonexistent_pet_returns_404(self, client: PetClient):
        """POST /pet/{petId} for a non-existent pet should return HTTP 404."""
        response = client.update_pet_with_form(
            pet_id=999_999_997,
            name="Ghost",
            status="available",
        )
        assert_status(response, 404)
