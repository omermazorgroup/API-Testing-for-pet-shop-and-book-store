from fix_API_testing.pet_store.models.pet import Pet
from fix_API_testing.pet_store.api.base_api import BaseApi


class PetApi(BaseApi):
    def __init__(self, url: str):
        super().__init__(url)

    def put_pet(self, pet):
        pet_data = pet.to_json()
        res = self._session.put(url=f"{self._url}/pet", data=pet_data)
        return res

    def post_new_pet(self, pet):
        pet_data = pet.to_json()
        res = self._session.post(url=f"{self._url}/pet", data=pet_data)
        return res

    def post_pet_by_id_and_update(self, pet_id: int, name: str, status: str):
        res = self._session.post(url=f"{self._url}/pet/{pet_id}?name={name}&status={status}")
        return res

    def get_pet_by_id(self, pet_id: int):
        res = self._session.get(url=f"{self._url}/pet/{pet_id}")
        return res

    def get_pets_by_status(self, status) -> [Pet]:
        res = self._session.get(url=f"{self._url}/pet/findByStatus?status={status}")
        return res

    def get_pet_by_tags(self, tags):
        tagsString = f'tags={tags[0]}'
        if not isinstance(tags, list):
            raise TypeError("tags must be a list of strings!")
        if len(tags) > 1:
            for tag in range(1, len(tags)):
                if not isinstance(tags[tag], str):
                    raise TypeError("one or more of the tags is not a string!")
                tagsString += f'&tags={tags[tag]}'
        res = self._session.get(url=f"{self._url}/pet/findByTags?{tagsString}")
        return res

    def upload_image_by_id(self, pet_id: int, files):
        res = self._session.post(url=f"{self._url}/pet/{pet_id}/uploadImage", files=files)
        return res

    def delete_pet_by_id(self, pet_id: int):
        res = self._session.delete(url=f"{self._url}/pet/{pet_id}")
        return res
