import json
import os
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
TEMPLATE_FOLDER_ID = "https://repo.metadatacenter.orgx/folders/6afcac2e-1b82-4484-a3f6-2327989ea698"  # YOUR FOLDER ID HERE
TOTAL_TEMPLATES = 60000


def read_template_from_fs():
    with open('empty-template.json', 'r') as file:
        return json.load(file)


def create_templates(template_data):
    start_time = time.time()

    formatted_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    print(f"Start time: {formatted_start_time}\n")

    for i in range(1, TOTAL_TEMPLATES + 1):
        elapsed_time = time.time() - start_time
        estimated_total_time = elapsed_time * TOTAL_TEMPLATES / i
        remaining_time = estimated_total_time - elapsed_time

        if i % 20 == 0:
            print(
                f"Generating template {i}/{TOTAL_TEMPLATES}. Estimated time left: {int(remaining_time // 60)} minutes {int(remaining_time % 60)} seconds.")

        template_data['schema:name'] = f"Test Template {i}"
        encoded_folder_id = urllib.parse.quote_plus(TEMPLATE_FOLDER_ID)
        response = requests.post(f"{BASE_URL}templates?folder_id={encoded_folder_id}", headers=HEADERS, json=template_data, verify=False)
        response.raise_for_status()

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


def main():
    template_data = read_template_from_fs()
    create_templates(template_data)


if __name__ == "__main__":
    main()
