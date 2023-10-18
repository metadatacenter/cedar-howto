import json

import requests.packages.urllib3

from org.metadatacenter.cedar.api.CedarAPI import CedarAPI
from settings import CEDAR_HOST, API_KEY

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def main():
    cedar = CedarAPI(CEDAR_HOST, API_KEY)
    cedar_category_api = cedar.get_category_api()
    # cedar_category_api.set_debug(True)
    category_tree_reponse = cedar_category_api.get_tree()
    print(json.dumps(category_tree_reponse.response_body, indent=2))


if __name__ == "__main__":
    main()
