"""
Shared assertion helpers.

Centralising common checks (status code, schema shape) keeps test files
lean and makes failures report a single, descriptive message.
"""
from __future__ import annotations

from requests import Response


def assert_status(response: Response, expected: int) -> None:
    """Assert HTTP status code with a helpful failure message."""
    assert response.status_code == expected, (
        f"Expected HTTP {expected}, got {response.status_code}.\n"
        f"URL: {response.url}\n"
        f"Body: {response.text}"
    )


def assert_pet_schema(body: dict) -> None:
    """Assert the response body contains the required Pet fields."""
    required_fields = {"id", "name", "status", "photoUrls"}
    missing = required_fields - body.keys()
    assert not missing, f"Pet response is missing fields: {missing}"


def assert_pet_matches(body: dict, **expected_fields) -> None:
    """Assert specific fields on a pet response body match expected values."""
    for field, expected_value in expected_fields.items():
        # Map pythonic field names to API camelCase where needed
        api_field = {"photo_urls": "photoUrls"}.get(field, field)
        actual = body.get(api_field)
        assert actual == expected_value, (
            f"Field '{api_field}': expected '{expected_value}', got '{actual}'"
        )
