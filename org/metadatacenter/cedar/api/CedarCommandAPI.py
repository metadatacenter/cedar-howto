import requests

from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.api.CedarSpecializedAPI import CedarSpecializedAPI
from org.metadatacenter.cedar.response.CedarResponse import CedarResponse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class CedarCommandAPI(CedarSpecializedAPI):
    def __init__(self, host, api_key):
        super().__init__(CedarResourceType.NONE, host, api_key)
        self.base_url = f"{self.resource_base_url}command"

    def move_resource_to_folder(self, source_id: str, target_folder_id: str):
        url = self.base_url + '/' + 'move-resource-to-folder'
        self.debug_request_header('POST', url=url)
        request_body = {
            '@id': source_id,
            'targetFolderId': target_folder_id
        }
        try:
            response = requests.post(url, headers=self.headers, json=request_body, verify=False)
            response.raise_for_status()
            self.last_created = response.json()
            self.last_response = CedarResponse(
                status_code=response.status_code,
                status_message='Success',
                response_body=self.last_created
            )

        except requests.exceptions.RequestException as err:
            self.last_created = None
            self.last_response = CedarResponse(
                status_code=err.response.status_code if err.response is not None else 'Unknown',
                status_message='Error',
                response_body=err.response.json() if err.response is not None else 'Unknown'
            )
        self.debug_response_header()
        if self.debug:
            print('Response.status_code:   ', self.last_response.status_code)
            print('Response.status_message:', self.last_response.status_message)

        return self.last_response
