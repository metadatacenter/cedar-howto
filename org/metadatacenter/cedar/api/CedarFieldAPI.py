import requests

from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.api.CedarSpecializedAPI import CedarSpecializedAPI

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class CedarFieldAPI(CedarSpecializedAPI):
    def __init__(self, host, api_key):
        super().__init__(CedarResourceType.FIELD, host, api_key)

    def create_field(self, folder_id=None):
        return super().create_artifact(folder_id)

    def create_field_with_id(self, at_id, folder_id=None):
        return super().create_artifact_with_id(at_id, folder_id)
