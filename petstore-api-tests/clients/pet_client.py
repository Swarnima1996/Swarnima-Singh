"""
PetClient — HTTP client for the /pet endpoints.

This layer is the only place that knows about HTTP verbs, headers,
and URLs.  Test files import this client and never call requests directly,
which means changing the base URL or adding auth is a single-file change.
"""
from __future__ import annotations

import requests
from requests import Response

from config import config
from models import Pet


class PetClient:
    """Thin wrapper around the /pet API endpoints."""

    def __init__(self, base_url: str = config.BASE_URL, timeout: int = config.REQUEST_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api_key": config.API_KEY,
        })

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def add_pet(self, pet: Pet) -> Response:
        """POST /pet — Add a new pet to the store."""
        return self._session.post(
            f"{self.base_url}/pet",
            json=pet.to_dict(),
            timeout=self.timeout,
        )

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    def get_pet_by_id(self, pet_id: int) -> Response:
        """GET /pet/{petId} — Find pet by ID."""
        return self._session.get(
            f"{self.base_url}/pet/{pet_id}",
            timeout=self.timeout,
        )

    def find_pets_by_status(self, status: str) -> Response:
        """GET /pet/findByStatus — Returns pets by status."""
        return self._session.get(
            f"{self.base_url}/pet/findByStatus",
            params={"status": status},
            timeout=self.timeout,
        )

    def find_pets_by_tags(self, tags: list[str]) -> Response:
        """GET /pet/findByTags — Returns pets by tags."""
        return self._session.get(
            f"{self.base_url}/pet/findByTags",
            params={"tags": tags},
            timeout=self.timeout,
        )

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update_pet(self, pet: Pet) -> Response:
        """PUT /pet — Update an existing pet."""
        return self._session.put(
            f"{self.base_url}/pet",
            json=pet.to_dict(),
            timeout=self.timeout,
        )

    def update_pet_with_form(self, pet_id: int, name: str, status: str) -> Response:
        """POST /pet/{petId} — Updates a pet in the store with form data.

        This endpoint expects application/x-www-form-urlencoded, not JSON.
        The Content-Type header is overridden per-request so the session-level
        JSON header does not interfere.
        """
        return self._session.post(
            f"{self.base_url}/pet/{pet_id}",
            data={"name": name, "status": status},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=self.timeout,
        )

    def get_pet_by_raw_id(self, pet_id: str) -> Response:
        """GET /pet/{petId} — Accepts a raw string ID for invalid-input testing."""
        return self._session.get(
            f"{self.base_url}/pet/{pet_id}",
            timeout=self.timeout,
        )

    def delete_pet_by_raw_id(self, pet_id: str) -> Response:
        """DELETE /pet/{petId} — Accepts a raw string ID for invalid-input testing."""
        return self._session.delete(
            f"{self.base_url}/pet/{pet_id}",
            timeout=self.timeout,
        )

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def delete_pet(self, pet_id: int) -> Response:
        """DELETE /pet/{petId} — Deletes a pet."""
        return self._session.delete(
            f"{self.base_url}/pet/{pet_id}",
            timeout=self.timeout,
        )