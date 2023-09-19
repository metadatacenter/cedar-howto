import json
import os
import time
import urllib.parse

import requests

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class ResourceHandler:
    def __init__(self, resource_type, empty_file):
        self.resource_type = resource_type
        self.empty_file = empty_file

        # Get the environment variables and validate
        CEDAR_HOST = os.environ.get('CEDAR_HOST')
        API_KEY = os.environ.get('CEDAR_TEST_USER_API_KEY')
        self.target_folder_id = os.environ.get('CEDAR_TARGET_FOLDER_ID')

        # Ensure required environment variables are set
        if not all([CEDAR_HOST, API_KEY, self.target_folder_id]):
            raise ValueError("Missing required environment variables: CEDAR_HOST, CEDAR_TEST_USER_API_KEY, or CEDAR_TARGET_FOLDER_ID.")

        self.base_url = f'https://resource.{CEDAR_HOST}/'
        self.headers = {
            'Authorization': f'apiKey {API_KEY}',
            'Content-Type': 'application/json'
        }
        self.delay_between_retries = 0.5

    def read_resource_from_fs(self):
        with open(self.empty_file, 'r') as file:
            return json.load(file)

    def create_resources(self, total_resources: int, batch_size: int = 20, max_retries: int = 3):
        start_time = time.time()
        execution_times = []

        resource_data = self.read_resource_from_fs()

        formatted_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
        print(f"Start time: {formatted_start_time}\n")

        for i in range(0, total_resources):
            elapsed_time = time.time() - start_time
            if i > 0:
                estimated_total_time = elapsed_time * total_resources / i
                remaining_time = estimated_total_time - elapsed_time
            else:
                estimated_total_time = 0
                remaining_time = 0

            resource_start_time = time.time()

            resource_data['schema:name'] = f"Test {self.resource_type.capitalize()} {i}"
            encoded_folder_id = urllib.parse.quote_plus(self.target_folder_id)

            for attempt in range(max_retries):
                try:
                    response = requests.post(f"{self.base_url}{self.resource_type}?folder_id={encoded_folder_id}", headers=self.headers, json=resource_data, verify=False)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as err:
                    print(f"Error on {self.resource_type} {i}: {err}. Attempt {attempt + 1}/{max_retries}.")
                    if attempt < max_retries - 1:
                        time.sleep(self.delay_between_retries)
                    else:
                        print(f"Failed to create {self.resource_type} {i} after {max_retries} attempts.")

            resource_end_time = time.time()
            execution_times.append(resource_end_time - resource_start_time)

            # Report the times
            if i % batch_size == 0 and i > 0:
                print('-' * 80)
                print(
                    f"Generated {self.resource_type} {i}/{total_resources}. Estimated time left: {int(remaining_time // 60)} minutes {int(remaining_time % 60)} seconds.")
                last_batch_average = sum(execution_times[-batch_size:]) / batch_size if execution_times else 0
                overall_average = sum(execution_times) / len(execution_times) if execution_times else 0

                print(f"\nAverage execution time for the last batch of {batch_size}: {last_batch_average:.2f} seconds.")
                print(f"Overall average execution time: {overall_average:.2f} seconds.")

                expected_end_time = time.time() + remaining_time
                formatted_expected_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expected_end_time))
                print(f"\nExpected end time after {i} {self.resource_type}: {formatted_expected_end_time}")

        # At the end, report the start time, the end time, the running time, and the average time per resource
        end_time = time.time()
        formatted_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
        running_time = end_time - start_time
        avg_time_per_resource = running_time / total_resources

        print(f"\nStart time: {formatted_start_time}")
        print(f"End time: {formatted_end_time}")
        print(f"Total running time: {running_time:.2f} seconds")
        print(f"Average time per {self.resource_type}: {avg_time_per_resource:.2f} seconds")
