import json
import os

import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

CEDAR_HOST = os.environ.get('CEDAR_HOST')
BASE_URL = f'https://resource.{CEDAR_HOST}/'
API_KEY = os.environ.get("CEDAR_ADMIN_USER_API_KEY")
HEADERS = {
    "Authorization": f"apiKey {API_KEY}",
    "Content-Type": "application/json"
}


def get_category_tree():
    response = requests.get(f"{BASE_URL}categories/tree", headers=HEADERS, verify=False)
    if response.status_code == 200:
        return response.json()
    raise Exception("Failed to get category tree")


def main():
    category_tree = get_category_tree()
    print(json.dumps(category_tree, indent=2))


if __name__ == "__main__":
    main()
