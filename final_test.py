import requests
from datetime import datetime, timedelta
import time

# Define the format for the allocated time
time_format = '%Y-%m-%d %H:%M:%S'

# Define time constraints
start_time = datetime.strptime("2023-12-19 10:00:00", time_format)
end_time = datetime.strptime("2023-12-19 17:00:00", time_format)
time_increment = timedelta(minutes=20)

# Initialize the latest processed ID
latest_processed_id = 0

while True:
    # Make the API request to get existing data
    api_url_getdata = "https://digitilize-pragun.onrender.com/server3/getdata"
    response_getdata = requests.get(api_url_getdata)

    # Check if the request was successful (status code 200)
    if response_getdata.status_code == 200:
        # Parse the JSON response
        existing_data = response_getdata.json()

        # Loop through the existing data and assign allocated time
        for i, patient_data in enumerate(existing_data["data"]):
            patient_id = patient_data["id"]

            # Check if the ID has already been processed
            if patient_id <= latest_processed_id:
                continue

            # Assign the formatted time
            formatted_allocated_time = start_time.strftime(time_format)
            patient_data["allocated_time"] = formatted_allocated_time

            # Make individual POST request for the new patient ID
            api_url_postdata = "https://digitilize-pragun.onrender.com/server3/postdata"
            update_response = requests.post(api_url_postdata, json={"id": patient_id, "allocated_time": formatted_allocated_time})

            if update_response.status_code == 201:
                print(f'Data successfully updated for ID {patient_id}')
                # Update the latest processed ID
                latest_processed_id = patient_id
            else:
                print(f'Error updating data for ID {patient_id}. Status code: {update_response.status_code}')
                print(update_response.text)  # Print the response content for further details

            # Increment time for every second ID
            if i % 2 == 1:
                start_time += time_increment

    else:
        # Print an error message if the request to get data was not successful
        print(f"Error: {response_getdata.status_code}")

    # Delay before the next iteration (adjust as needed)
    time.sleep(10)
