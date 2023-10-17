from http import HTTPStatus

from org.metadatacenter.cedar.api.CedarAPI import CedarAPI
from settings import CEDAR_HOST, API_KEY

if __name__ == "__main__":
    cedar = CedarAPI(CEDAR_HOST, API_KEY)
    cedar_field_api = cedar.get_field_api()
    # cedar_field_api.set_debug(True)
    cedar_field_api.load_artifact_from_file('./input-files/simple-field-unsaved.json')
    cedar_response = cedar_field_api.create_field()
    if cedar_response.status_code == HTTPStatus.CREATED:
        print('Field was created')
        at_id = cedar_field_api.get_created_at_id()
        print('Created @id:', at_id)
    else:
        print('There was an error while creating the field')
        print(cedar_response.status_code, cedar_response.status_message)
        print(cedar_response.response_body)
