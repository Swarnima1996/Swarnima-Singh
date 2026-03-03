""""
Tests for CREATE operations — POST /pet
"""
import pytest

from clients import PetClient
from models import Pet, PetFactory
from utils import assert_status, assert_pet_schema, assert_pet_matches


@pytest.mark.create
@pytest.mark.smoke
class TestCreatePet:

    def test_create_pet_returns_200(self, tracked_client):
        """POST /pet with a valid payload should return HTTP 200."""
        client, created_ids = tracked_client
        pet = PetFactory.build()
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert_status(response, 200)

    def test_create_pet_response_has_required_fields(self, tracked_client):
        """Response body must contain all required Pet fields."""
        client, created_ids = tracked_client
        pet = PetFactory.build()
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert_status(response, 200)
        assert_pet_schema(response.json())

    def test_create_pet_persists_name(self, tracked_client):
        """The name provided in the request body must be returned in the response."""
        client, created_ids = tracked_client
        pet = PetFactory.build()
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert_status(response, 200)
        assert_pet_matches(response.json(), name=pet.name)

    def test_create_pet_persists_status(self, tracked_client):
        """The status provided in the request body must be returned in the response."""
        client, created_ids = tracked_client
        pet = PetFactory.build()
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert_status(response, 200)
        assert_pet_matches(response.json(), status=pet.status)

    def test_create_pet_assigns_id(self, tracked_client):
        """A valid integer id must be present in the response body."""
        client, created_ids = tracked_client
        pet = PetFactory.build()
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert_status(response, 200)
        body = response.json()
        assert "id" in body, "Response is missing 'id' field"
        assert isinstance(body["id"], int), f"'id' should be an integer, got {type(body['id'])}"

    def test_create_pet_with_all_statuses(self, tracked_client):
        """Pets can be created with each of the valid status values."""
        client, created_ids = tracked_client
        for status in ("available", "pending", "sold"):
            pet = PetFactory.build(status=status)
            response = client.add_pet(pet)
            if response.status_code == 200:
                created_ids.append(response.json()["id"])
            assert_status(response, 200)
            assert_pet_matches(response.json(), status=status)

    def test_create_pet_with_category(self, tracked_client):
        """A pet created with a category should return that category in the response."""
        client, created_ids = tracked_client
        pet = PetFactory.build(with_category=True)
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert_status(response, 200)
        body = response.json()
        assert "category" in body, "Response missing 'category'"
        assert body["category"]["name"] == pet.category.name

    def test_create_pet_with_tags(self, tracked_client):
        """A pet created with tags should return those tags in the response."""
        client, created_ids = tracked_client
        pet = PetFactory.build(with_tags=True)
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert_status(response, 200)
        body = response.json()
        assert "tags" in body and len(body["tags"]) > 0, "Response missing 'tags'"

    def test_create_pet_returns_json_content_type(self, tracked_client):
        """Response Content-Type should be application/json."""
        client, created_ids = tracked_client
        pet = PetFactory.build()
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert_status(response, 200)
        assert "application/json" in response.headers.get("Content-Type", ""), (
            f"Expected JSON Content-Type, got: {response.headers.get('Content-Type')}"
        )

    @pytest.mark.negative
    def test_create_pet_with_invalid_status(self, tracked_client):
        """Posting a pet with an invalid status value should not return 200."""
        client, created_ids = tracked_client
        pet = PetFactory.build(status="flying")
        response = client.add_pet(pet)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
        assert response.status_code != 200, (
            "Expected a non-200 response for an invalid status value, but got 200"
        )