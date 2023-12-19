import requests
from datetime import datetime, timedelta

# Make the API request to get existing data
api_url_getdata = "https://digitilize-pragun.onrender.com/server3/getdata"
response_getdata = requests.get(api_url_getdata)

# Check if the request was successful (status code 200)
if response_getdata.status_code == 200:
    # Parse the JSON response
    existing_data = response_getdata.json()

    # Define the format for the allocated time
    time_format = '%Y-%m-%d %H:%M:%S'

    # Define time constraints
    start_time = datetime.strptime("2023-12-19 10:00:00", time_format)
    end_time = datetime.strptime("2023-12-19 17:00:00", time_format)
    time_increment = timedelta(minutes=20)

    # Initialize a list to store the updated allocated times
    updated_times = []

    # Loop through the existing data and assign allocated time
    for i, patient_data in enumerate(existing_data["data"]):
        patient_id = patient_data["id"]

        # Assign the formatted time
        formatted_allocated_time = start_time.strftime(time_format)
        patient_data["allocated_time"] = formatted_allocated_time

        # Append the updated time to the list
        updated_times.append({"id": patient_id, "allocated_time": formatted_allocated_time})

        # Increment time for every second ID
        if i % 2 == 1:
            start_time += time_increment

    # Print the resulting allocated times
    for updated_time in updated_times:
        print(updated_time)


else:
    # Print an error message if the request was not successful
    print(f"Error: {response_getdata.status_code}")
