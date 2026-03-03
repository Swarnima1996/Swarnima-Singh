"""
Pet data model.

Uses a dataclass for clean, typed representation of a Pet resource.
The PetFactory provides convenient methods for generating test data.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field, asdict
from typing import Optional

from faker import Faker

fake = Faker()


@dataclass
class Category:
    id: int
    name: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Tag:
    id: int
    name: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Pet:
    name: str
    status: str
    id: Optional[int] = None
    category: Optional[Category] = None
    photo_urls: list[str] = field(default_factory=list)
    tags: list[Tag] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = {
            "name": self.name,
            "status": self.status,
            "photoUrls": self.photo_urls,
        }
        if self.id is not None:
            payload["id"] = self.id
        if self.category:
            payload["category"] = self.category.to_dict()
        if self.tags:
            payload["tags"] = [t.to_dict() for t in self.tags]
        return payload


class PetFactory:
    """Factory for generating Pet test data."""

    @staticmethod
    def build(
        name: Optional[str] = None,
        status: str = "available",
        pet_id: Optional[int] = None,
        with_category: bool = True,
        with_tags: bool = True,
    ) -> Pet:
        """Build a Pet instance with sensible test defaults."""
        category = (
            Category(id=random.randint(1, 10), name=fake.word().capitalize())
            if with_category
            else None
        )
        tags = (
            [Tag(id=random.randint(1, 100), name=fake.word()) for _ in range(2)]
            if with_tags
            else []
        )
        return Pet(
            id=pet_id or random.randint(100_000, 999_999),
            name=name or f"{fake.first_name()}-{fake.word()}",
            status=status,
            photo_urls=["https://example.com/photo.jpg"],
            category=category,
            tags=tags,
        )

    @staticmethod
    def build_minimal(name: str = "TestPet", status: str = "available") -> Pet:
        """Build a Pet with only required fields (name, status, photoUrls)."""
        return Pet(
            name=name,
            status=status,
            photo_urls=["https://example.com/photo.jpg"],
        )
