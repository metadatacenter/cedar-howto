import json
import os
import time
import urllib.parse  # For URL encoding

import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

CEDAR_HOST = os.environ.get('CEDAR_HOST')
BASE_URL = f'https://resource.{CEDAR_HOST}/'
API_KEY = os.environ.get('CEDAR_TEST_USER_API_KEY')
TARGET_FOLDER_ID = os.environ.get('CEDAR_TARGET_FOLDER_ID')
HEADERS = {
    'Authorization': f'apiKey {API_KEY}',
    'Content-Type': 'application/json'
}
MAX_RETRIES = 3
DELAY_BETWEEN_RETRIES = 2
BATCH_SIZE = 20
TOTAL_TEMPLATES = 50000


def read_template_from_fs():
    with open('empty-template.json', 'r') as file:
        return json.load(file)


def create_templates(template_data):
    start_time = time.time()
    execution_times = []

    formatted_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    print(f"Start time: {formatted_start_time}\n")

    for i in range(0, TOTAL_TEMPLATES):
        elapsed_time = time.time() - start_time
        if i > 0:
            estimated_total_time = elapsed_time * TOTAL_TEMPLATES / i
            remaining_time = estimated_total_time - elapsed_time
        else:
            estimated_total_time = 0
            remaining_time = 0
        template_start_time = time.time()

        template_data['schema:name'] = f"Test Template {i}"
        encoded_folder_id = urllib.parse.quote_plus(TARGET_FOLDER_ID)

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(f"{BASE_URL}templates?folder_id={encoded_folder_id}", headers=HEADERS, json=template_data, verify=False)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as err:
                print(f"Error on template {i}: {err}. Attempt {attempt + 1}/{MAX_RETRIES}.")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN_RETRIES)
                else:
                    print(f"Failed to create template {i} after {MAX_RETRIES} attempts.")

        template_end_time = time.time()
        execution_times.append(template_end_time - template_start_time)

        # Report the times
        if i % BATCH_SIZE == 0 and i > 0:
            print('-' * 80)
            print(f"Generated template {i}/{TOTAL_TEMPLATES}. Estimated time left: {int(remaining_time // 60)} minutes {int(remaining_time % 60)} seconds.")
            last_batch_average = sum(execution_times[-BATCH_SIZE:]) / BATCH_SIZE if execution_times else 0
            overall_average = sum(execution_times) / len(execution_times) if execution_times else 0

            print(f"\nAverage execution time for the last batch of {BATCH_SIZE}: {last_batch_average:.2f} seconds.")
            print(f"Overall average execution time:                  {overall_average:.2f} seconds.")

            expected_end_time = time.time() + remaining_time
            formatted_expected_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expected_end_time))
            print(f"\nExpected end time after {i} templates: {formatted_expected_end_time}")

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
