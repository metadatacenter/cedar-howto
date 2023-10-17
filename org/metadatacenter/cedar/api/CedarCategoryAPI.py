import requests

from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.api.CedarSpecializedAPI import CedarSpecializedAPI
from org.metadatacenter.cedar.response.CedarResponse import CedarResponse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class CedarCategoryAPI(CedarSpecializedAPI):
    def __init__(self, host, api_key):
        super().__init__(CedarResourceType.CATEGORY, host, api_key)

    def get_tree(self):
        url = self.base_url + '/' + 'tree'
        self.debug_request_header('GET', url=url)
        try:
            response = requests.get(url, headers=self.headers, verify=False)
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

    def create_category(self, name, description, parent_id):
        self.loaded_json = {
            "schema:name": name,
            "schema:description": description,
            "parentCategoryId": parent_id,
        }
        print(self.loaded_json)
        return super().create_artifact()
