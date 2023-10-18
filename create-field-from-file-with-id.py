import json
from http import HTTPStatus

from org.metadatacenter.cedar.api.CedarAPI import CedarAPI
from settings import CEDAR_HOST, API_KEY

if __name__ == "__main__":
    cedar = CedarAPI(CEDAR_HOST, API_KEY)
    cedar_field_api = cedar.get_field_api()
    # cedar_field_api.set_debug(True)
    cedar_field_api.load_artifact_from_file('./input-files/simple-field-saved.json')
    at_id = cedar_field_api.generate_at_id()
    print('Generated @id:', at_id)
    cedar_field_api.set_at_id(at_id)
    # print(json.dumps(cedar_field_api.loaded_json, indent=4))
    cedar_response = cedar_field_api.create_field_with_id(at_id)
    if cedar_response.status_code == HTTPStatus.CREATED:
        print('Field was created')
        at_id = cedar_field_api.get_created_at_id()
        print('Created @id:', at_id)
    else:
        print('There was an error while creating the field')
        print(cedar_response.status_code, cedar_response.status_message)
        json_str = json.dumps(cedar_response.response_body, indent=4)
        print(json_str)
