import json
import os
import random
import time
import urllib.parse  # For URL encoding

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
TEMPLATE_FOLDER_ID = "https://repo.metadatacenter.orgx/folders/XYZ"  # YOUR FOLDER ID HERE
TOTAL_TEMPLATES = 100
MAX_RANDOM_CATEGORY_COUNT = 5


def get_all_categories():
    categories = []
    response = requests.get(f"{BASE_URL}categories/tree", headers=HEADERS, verify=False)
    response.raise_for_status()
    tree = response.json()

    def extract_categories(node):
        categories.append(node)
        for child in node['children']:
            extract_categories(child)

    extract_categories(tree)
    return categories


def read_template_from_fs():
    with open('empty-template.json', 'r') as file:
        return json.load(file)


def create_templates(template_data, categories):
    used_categories_names = set()
    start_time = time.time()

    formatted_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    print(f"Start time: {formatted_start_time}\n")

    for i in range(1, TOTAL_TEMPLATES + 1):
        elapsed_time = time.time() - start_time
        estimated_total_time = elapsed_time * TOTAL_TEMPLATES / i
        remaining_time = estimated_total_time - elapsed_time

        print(
            f"Generating template {i}/{TOTAL_TEMPLATES}. Estimated time left: {int(remaining_time // 60)} minutes {int(remaining_time % 60)} seconds.")

        template_data['schema:name'] = f"Test Template {i}"
        encoded_folder_id = urllib.parse.quote_plus(TEMPLATE_FOLDER_ID)
        response = requests.post(f"{BASE_URL}templates?folder_id={encoded_folder_id}", headers=HEADERS, json=template_data, verify=False)
        response.raise_for_status()
        new_template_id = response.json()['@id']

        num_categories = random.randint(1, MAX_RANDOM_CATEGORY_COUNT)
        chosen_categories = random.sample(categories, num_categories)
        category_ids = [category['@id'] for category in chosen_categories]

        attach_categories_to_template(new_template_id, category_ids)

        for category in chosen_categories:
            used_categories_names.add(category['schema:name'])

        # Every 20 templates, report the expected end time
        if i % 20 == 0:
            expected_end_time = time.time() + remaining_time
            formatted_expected_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expected_end_time))
            print(f"\nExpected end time after {i} templates: {formatted_expected_end_time}\n")

    # At the end, report the start time, the end time, the running time, and the average time per template
    end_time = time.time()
    formatted_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
    running_time = end_time - start_time
    avg_time_per_template = running_time / TOTAL_TEMPLATES

    print(f"\nStart time: {formatted_start_time}")
    print(f"End time:     {formatted_end_time}")
    print(f"Total running time:        {running_time:.2f} seconds")
    print(f"Average time per template: {avg_time_per_template:.2f} seconds")

    return used_categories_names


def attach_categories_to_template(template_id, category_ids):
    data = {
        "artifactId": template_id,
        "categoryIds": category_ids
    }
    response = requests.post(f"{BASE_URL}command/attach-categories", headers=HEADERS, json=data, verify=False)  # Endpoint changed
    response.raise_for_status()


def main():
    categories = get_all_categories()
    template_data = read_template_from_fs()
    used_categories_names = create_templates(template_data, categories)

    print("\nUsed Categories:")
    for name in used_categories_names:
        print(name)


if __name__ == "__main__":
    main()
