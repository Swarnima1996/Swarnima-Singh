"""
Tests for CREATE operations — POST /pet
"""
import pytest

from clients import PetClient
from models import Pet, PetFactory
from utils import assert_status, assert_pet_schema, assert_pet_matches


@pytest.mark.create
@pytest.mark.smoke
class TestCreatePet:

    def test_create_pet_returns_200(self, client: PetClient, pet_payload: Pet):
        """POST /pet with a valid payload should return HTTP 200."""
        response = client.add_pet(pet_payload)
        assert_status(response, 200)

    def test_create_pet_response_has_required_fields(self, client: PetClient, pet_payload: Pet):
        """Response body must contain all required Pet fields."""
        response = client.add_pet(pet_payload)
        assert_status(response, 200)
        assert_pet_schema(response.json())

    def test_create_pet_persists_name(self, client: PetClient, pet_payload: Pet):
        """The name provided in the request body must be returned in the response."""
        response = client.add_pet(pet_payload)
        assert_status(response, 200)
        assert_pet_matches(response.json(), name=pet_payload.name)

    def test_create_pet_persists_status(self, client: PetClient, pet_payload: Pet):
        """The status provided in the request body must be returned in the response."""
        response = client.add_pet(pet_payload)
        assert_status(response, 200)
        assert_pet_matches(response.json(), status=pet_payload.status)

    def test_create_pet_assigns_id(self, client: PetClient, pet_payload: Pet):
        """A valid integer id must be present in the response body."""
        response = client.add_pet(pet_payload)
        assert_status(response, 200)
        body = response.json()
        assert "id" in body, "Response is missing 'id' field"
        assert isinstance(body["id"], int), f"'id' should be an integer, got {type(body['id'])}"

    def test_create_pet_with_all_statuses(self, client: PetClient):
        """Pets can be created with each of the valid status values."""
        for status in ("available", "pending", "sold"):
            pet = PetFactory.build(status=status)
            response = client.add_pet(pet)
            assert_status(response, 200)
            assert_pet_matches(response.json(), status=status)

    def test_create_pet_with_category(self, client: PetClient):
        """A pet created with a category should return that category in the response."""
        pet = PetFactory.build(with_category=True)
        response = client.add_pet(pet)
        assert_status(response, 200)
        body = response.json()
        assert "category" in body, "Response missing 'category'"
        assert body["category"]["name"] == pet.category.name

    def test_create_pet_with_tags(self, client: PetClient):
        """A pet created with tags should return those tags in the response."""
        pet = PetFactory.build(with_tags=True)
        response = client.add_pet(pet)
        assert_status(response, 200)
        body = response.json()
        assert "tags" in body and len(body["tags"]) > 0, "Response missing 'tags'"

    def test_create_pet_returns_json_content_type(self, client: PetClient, pet_payload: Pet):
        """Response Content-Type should be application/json."""
        response = client.add_pet(pet_payload)
        assert_status(response, 200)
        assert "application/json" in response.headers.get("Content-Type", ""), (
            f"Expected JSON Content-Type, got: {response.headers.get('Content-Type')}"
        )

    @pytest.mark.negative
    def test_create_pet_with_invalid_status(self, client: PetClient):
        """Posting a pet with an invalid status value should not return 200."""
        pet = PetFactory.build(status="flying")
        response = client.add_pet(pet)
        # The spec defines only available/pending/sold — an invalid value should be rejected
        assert response.status_code != 200, (
            "Expected a non-200 response for an invalid status value, but got 200"
        )
