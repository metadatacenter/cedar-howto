import json
from abc import ABC
from urllib.parse import quote

import requests
import uuid

from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.response.CedarResponse import CedarResponse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class CedarSpecializedAPI(ABC):
    def __init__(self, resource_type: CedarResourceType, host: str, api_key: str):
        self.resource_type = resource_type
        self.host = host if host.endswith('/') else f"{host}/"
        self.resource_base_url = f'https://resource.{self.host}'
        self.repo_base_url = f'https://repo.{self.host}'
        self.base_url = f"{self.resource_base_url}{resource_type.value['prefix']}"

        self.api_key = api_key
        self.headers = {
            'Authorization': f'apiKey {self.api_key}',
            'Content-Type': 'application/json'
        }

        self.loaded_json = None
        self.last_response = None
        self.last_created = None
        self.debug = False

    def load_artifact_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.loaded_json = json.load(file)

    def set_debug(self, debug):
        self.debug = debug

    def get_created_at_id(self):
        if self.last_created is not None:
            return self.last_created.get('@id', None)
        else:
            return None

    def generate_at_id(self):
        prefix = self.resource_type.value['prefix']
        uuid_str = str(uuid.uuid4())
        return f'{self.repo_base_url}{prefix}/{uuid_str}'

    def set_at_id(self, at_id):
        self.loaded_json['@id'] = at_id

    def debug_request_header(self, method, url=None):
        url_str = self.base_url if url is None else url
        if self.debug:
            print('Request URL:', url_str)
            print('Method:     ', method)
            print('Headers:    ', self.headers)

    def debug_response_header(self):
        if self.debug:
            print('Response.status_code:   ', self.last_response.status_code)
            print('Response.status_message:', self.last_response.status_message)

    def create_artifact(self):
        self.debug_request_header('POST')
        try:
            response = requests.post(self.base_url, headers=self.headers, json=self.loaded_json, verify=False)
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

        return self.last_response

    def create_artifact_with_id(self, at_id):
        url = self.base_url + '/' + quote(at_id, safe='')
        self.debug_request_header('POST', url=url)
        try:
            response = requests.put(url, headers=self.headers, json=self.loaded_json, verify=False)
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
