from http import HTTPStatus

from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.api.CedarAPI import CedarAPI
from org.metadatacenter.cedar.api.CedarCommandAPI import CedarCommandAPI
from org.metadatacenter.cedar.api.CedarFolderContentAPI import CedarFolderContentAPI
from settings import CEDAR_HOST, API_KEY, SOURCE_FOLDER_ID, TARGET_FOLDER_ID


def read_field_from_folder(folder_content_api: CedarFolderContentAPI, folder_id, page_size, current_offset):
    return folder_content_api.get_folder_content(folder_id, limit=page_size, offset=current_offset, resource_types=[CedarResourceType.FIELD])


def move_fields_one_by_one(command_api: CedarCommandAPI, content_list):
    print('Batch size:', content_response.get_resource_count())
    for artifact in content_list:
        print('Move')
        print('@id         ' + artifact['@id'])
        print('schema:name ' + artifact['schema:name'])
        print('-' * 40)
        cedar_response = command_api.move_resource_to_folder(artifact['@id'], TARGET_FOLDER_ID)
        if cedar_response.status_code == HTTPStatus.CREATED:
            print('Field was moved', artifact['@id'])
        else:
            print('There was an error while moving the field', artifact['@id'])
            print(cedar_response.status_code, cedar_response.status_message)
            print(cedar_response.response_body)


if __name__ == "__main__":
    cedar = CedarAPI(CEDAR_HOST, API_KEY)
    cedar_folder_content_api = cedar.get_folder_content_api()
    cedar_folder_content_api.set_debug(True)
    cedar_command_api = cedar.get_command_api()
    cedar_command_api.set_debug(True)
    page_size = 5
    current_offset = 0
    content_response = read_field_from_folder(cedar_folder_content_api, SOURCE_FOLDER_ID, page_size, current_offset)
    while content_response.get_resource_count() > 0:
        move_fields_one_by_one(cedar_command_api, content_response.get_resources())
        content_response = read_field_from_folder(cedar_folder_content_api, SOURCE_FOLDER_ID, page_size, current_offset)
