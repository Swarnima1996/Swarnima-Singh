from clients.pet_client import PetClient
from models.pet import Pet


def test_can_create_pet():
    client = PetClient()
    new_pet = Pet(name="MacTestPet", status="available")

    response = client.add_pet(new_pet)

    assert response.status_code == 200
    assert response.json()["name"] == "MacTestPet"
    print("\n✅ API is responding correctly!")