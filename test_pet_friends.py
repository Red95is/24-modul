from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Charlie', animal_type='Dog', age='3', pet_photo='images/charlie.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, "")
    if len(result['pets']) > 0:
        pet_id = result['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        assert status == 200
        _, result = pf.get_list_of_pets(auth_key, "")
        assert pet_id not in [pet['id'] for pet in result['pets']]
    else:
        raise Exception("No pets found to delete")

def test_update_pet_info(name='Max', animal_type='Cat', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, "")
    if len(result['pets']) > 0:
        pet_id = result['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        raise Exception("No pets found to update")
