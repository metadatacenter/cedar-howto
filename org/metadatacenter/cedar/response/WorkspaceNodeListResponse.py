import json

from org.metadatacenter.cedar.response.CedarResponse import CedarResponse


class WorkspaceNodeListResponse(CedarResponse):
    def __init__(self, status_code, status_message, response_body):
        super().__init__(status_code, status_message, response_body)
        self.resources = response_body['resources']
        self.paging = response_body['paging']
        self.path_info = response_body['pathInfo']

    def get_resource_count(self):
        return len(self.resources)

    def get_resources(self):
        return self.resources
