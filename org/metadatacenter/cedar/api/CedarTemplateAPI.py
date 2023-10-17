import requests

from org.metadatacenter.cedar.CedarResourceType import CedarResourceType
from org.metadatacenter.cedar.api.CedarSpecializedAPI import CedarSpecializedAPI

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class CedarTemplateAPI(CedarSpecializedAPI):
    def __init__(self, host, api_key):
        super().__init__(CedarResourceType.TEMPLATE, host, api_key)

    def create_template(self, folder_id=None):
        return super().create_artifact(folder_id)

    def create_template_with_id(self, at_id, folder_id=None):
        return super().create_artifact_with_id(at_id, folder_id)
