import json

import requests.packages.urllib3

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

from org.metadatacenter.cedar.api.CedarAPI import CedarAPI
from settings import CEDAR_HOST, API_KEY

from http import HTTPStatus


def get_nci_cadsr_category_id(cedar_category_api):
    tree_response = cedar_category_api.get_tree()
    tree = tree_response.response_body
    for child in tree['children']:
        if child['schema:name'] == 'NCI caDSR':
            return child['@id']
    raise ValueError("NCI caDSR category not found in the tree")


def create_category(cedar_category_api, name, description, parent_id):
    return cedar_category_api.create_category(name, description, parent_id)


def create_recursive_categories(cedar_category_api, name_prefix, description_prefix, parent_id, depth=1, max_depth=4, count=0, max_count=4000):
    if count >= max_count or depth > max_depth:
        return count

    for i in range(10):  # 10 categories per level to reach 4000 in 4 levels
        count += 1
        name = f"{name_prefix} {count}"
        description = f"{description_prefix} {count}"
        create_response = create_category(cedar_category_api, name, description, parent_id)
        if create_response.status_code == HTTPStatus.CREATED:
            new_category_id = cedar_category_api.get_created_at_id()
            count = create_recursive_categories(cedar_category_api, name_prefix, description_prefix, new_category_id, depth + 1, max_depth, count, max_count)
        else:
            print('There was an error while creating the category', name)
            print(json.dumps(create_response.response_body))

    return count


def main():
    cedar = CedarAPI(CEDAR_HOST, API_KEY)
    cedar_category_api = cedar.get_category_api()
    cedar_category_api.set_debug(True)

    nci_cadsr_id = get_nci_cadsr_category_id(cedar_category_api)
    create_recursive_categories(cedar_category_api, "Test Category", "Description Test Category", nci_cadsr_id)


if __name__ == "__main__":
    main()
