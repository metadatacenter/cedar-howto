import os

import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

CEDAR_HOST = os.environ.get('CEDAR_HOST')
BASE_URL = f'https://resource.{CEDAR_HOST}/'
API_KEY = os.environ.get('CEDAR_ADMIN_USER_API_KEY')
HEADERS = {
    'Authorization': f'apiKey {API_KEY}',
    'Content-Type': 'application/json'
}


def get_nci_cadsr_category_id():
    response = requests.get(f"{BASE_URL}categories/tree", headers=HEADERS, verify=False)
    if response.status_code != 200:
        raise ValueError("Failed to fetch the category tree", response.status_code)

    tree = response.json()
    for child in tree['children']:
        if child['schema:name'] == 'NCI caDSR':
            return child['@id']
    raise ValueError("NCI caDSR category not found in the tree")


def create_category(name, description, parent_id):
    data = {
        "schema:name": name,
        "schema:description": description,
        "parentCategoryId": parent_id,
    }
    response = requests.post(f"{BASE_URL}categories", headers=HEADERS, json=data, verify=False)
    if response.status_code != 201:
        raise ValueError(f"Failed to create category {name}")
    return response.json().get('@id')


def create_recursive_categories(name_prefix, description_prefix, parent_id, depth=1, max_depth=4, count=0, max_count=4000):
    if count >= max_count or depth > max_depth:
        return count

    for i in range(10):  # 10 categories per level to reach 4000 in 4 levels
        count += 1
        name = f"{name_prefix} {count}"
        description = f"{description_prefix} {count}"
        new_category_id = create_category(name, description, parent_id)
        count = create_recursive_categories(name_prefix, description_prefix, new_category_id, depth + 1, max_depth, count, max_count)
        print(count)

    return count


def main():
    nci_cadsr_id = get_nci_cadsr_category_id()
    create_recursive_categories("Test Category", "Description Test Category", nci_cadsr_id)


if __name__ == "__main__":
    main()
