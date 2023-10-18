import time
from http import HTTPStatus

from org.metadatacenter.cedar.api.CedarAPI import CedarAPI
from settings import CEDAR_HOST, API_KEY, TARGET_FOLDER_ID


def create_resources(total_resources: int, batch_size: int = 20, max_retries: int = 3):
    delay_between_retries = 0.5

    cedar = CedarAPI(CEDAR_HOST, API_KEY)
    cedar_element_api = cedar.get_element_api()
    # cedar_element_api.set_debug(True)
    cedar_element_api.load_artifact_from_file('./input-files/empty-element-unsaved.json')

    start_time = time.time()
    execution_times = []

    formatted_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    print(f"Start time: {formatted_start_time}\n")

    for i in range(0, total_resources):
        elapsed_time = time.time() - start_time
        if i > 0:
            estimated_total_time = elapsed_time * total_resources / i
            remaining_time = estimated_total_time - elapsed_time
        else:
            remaining_time = 0

        resource_start_time = time.time()

        cedar_element_api.set_top_node_value('schema:name', f"Test Element {i}")

        for attempt in range(max_retries):
            create_response = cedar_element_api.create_element(folder_id=TARGET_FOLDER_ID)
            if create_response.status_code == HTTPStatus.CREATED:
                break
            else:
                print(f"Error on artifact {i}: {create_response.status_code}. Attempt {attempt + 1}/{max_retries}.")
                if attempt < max_retries - 1:
                    time.sleep(delay_between_retries)
                else:
                    print(f"Failed to create artifact {i} after {max_retries} attempts.")

        resource_end_time = time.time()
        execution_times.append(resource_end_time - resource_start_time)

        if i % batch_size == 0 and i > 0:
            print('-' * 80)
            print(
                f"Generated artifact {i}/{total_resources}. Estimated time left: {int(remaining_time // 60)} minutes {int(remaining_time % 60)} seconds.")
            last_batch_average = sum(execution_times[-batch_size:]) / batch_size if execution_times else 0
            overall_average = sum(execution_times) / len(execution_times) if execution_times else 0

            print(f"\nAverage execution time for the last batch of {batch_size}: {last_batch_average:.2f} seconds.")
            print(f"Overall average execution time: {overall_average:.2f} seconds.")

            expected_end_time = time.time() + remaining_time
            formatted_expected_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expected_end_time))
            print(f"\nExpected end time after {i} artifacts: {formatted_expected_end_time}")

    end_time = time.time()
    formatted_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
    running_time = end_time - start_time
    avg_time_per_resource = running_time / total_resources

    print(f"\nStart time: {formatted_start_time}")
    print(f"End time: {formatted_end_time}")
    print(f"Total running time: {running_time:.2f} seconds")
    print(f"Average time per artifact: {avg_time_per_resource:.2f} seconds")


if __name__ == "__main__":
    create_resources(1000)
