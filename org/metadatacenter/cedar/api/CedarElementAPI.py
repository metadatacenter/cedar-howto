import requests

from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.api.CedarSpecializedAPI import CedarSpecializedAPI

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class CedarElementAPI(CedarSpecializedAPI):
    def __init__(self, host, api_key):
        super().__init__(CedarResourceType.ELEMENT, host, api_key)

    def create_element(self, folder_id=None):
        return super().create_artifact(folder_id)

    def create_element_with_id(self, at_id, folder_id=None):
        return super().create_artifact_with_id(at_id, folder_id)
