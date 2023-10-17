from typing import List
from urllib.parse import quote, urlencode, quote_plus

import requests

from org.metadatacenter.cedar.CedarPublicationStatusFilter import CedarPublicationStatusFilter
from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.CedarSortField import CedarSortField
from org.metadatacenter.cedar.api.CedarSpecializedAPI import CedarSpecializedAPI
from org.metadatacenter.cedar.response.CedarResponse import CedarResponse
from org.metadatacenter.cedar.response.WorkspaceNodeListResponse import WorkspaceNodeListResponse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class CedarFolderContentAPI(CedarSpecializedAPI):
    def __init__(self, host, api_key):
        super().__init__(CedarResourceType.FOLDER, host, api_key)

    def get_folder_content(self, source_folder_id: str, limit: int = 100, offset: int = 0,
                           resource_types: List[CedarResourceType] = [CedarResourceType.FOLDER, CedarResourceType.FIELD, CedarResourceType.ELEMENT,
                                                                      CedarResourceType.TEMPLATE, CedarResourceType.INSTANCE],
                           publication_status: CedarPublicationStatusFilter = CedarPublicationStatusFilter.ALL,
                           sort_by: List[CedarSortField] = [CedarSortField.NAME]):

        resource_type_values = [resource_type.value['value'] for resource_type in resource_types]
        resource_types_str = ','.join(resource_type_values)

        sort_type_values = [sort_type.value['value'] for sort_type in sort_by]
        sort_types_str = ','.join(sort_type_values)

        publication_status_str = publication_status.value['value']

        params = {
            'limit': limit,
            'offset': offset,
            'publication_status': publication_status_str,
            'resource_types': resource_types_str,
            'sort': sort_types_str
        }
        encoded_params = urlencode(params, quote_via=quote_plus)
        url = self.base_url + '/' + quote(source_folder_id, safe='') + '/contents' + '?' + encoded_params
        self.debug_request_header('GET', url=url)
        try:
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            self.last_created = response.json()
            self.last_response = WorkspaceNodeListResponse(
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
