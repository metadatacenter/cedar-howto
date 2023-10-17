from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.api.CedarAPI import CedarAPI
from org.metadatacenter.cedar.api.CedarFolderContentAPI import CedarFolderContentAPI
from settings import CEDAR_HOST, API_KEY, SOURCE_FOLDER_ID


def read_field_from_folder(folder_content_api: CedarFolderContentAPI, folder_id, page_size, current_offset):
    return folder_content_api.get_folder_content(folder_id, limit=page_size, offset=current_offset, resource_types=[CedarResourceType.FIELD])


def list_current_batch(content_response):
    print('Batch size:', content_response.get_resource_count())
    for artifact in content_response.get_resources():
        print('@id         ' + artifact['@id'])
        print('schema:name ' + artifact['schema:name'])
        print('-' * 40)


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
        list_current_batch(content_response)
        current_offset += page_size
        content_response = read_field_from_folder(cedar_folder_content_api, SOURCE_FOLDER_ID, page_size, current_offset)
