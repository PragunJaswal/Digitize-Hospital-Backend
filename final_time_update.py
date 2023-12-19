import requests
from datetime import datetime, timedelta

# Make the API request to get existing data
api_url_getdata = "https://digitilize-pragun.onrender.com/server3/getdata"
response_getdata = requests.get(api_url_getdata)

# Check if the request was successful (status code 200)
if response_getdata.status_code == 200:
    try:
        # Try to parse the JSON response
        existing_data = response_getdata.json()

        # Check if the response contains the "data" key
        if "data" in existing_data:
            # Create a dictionary to store existing allocated times as datetime objects
            existing_allocated_times = {}

            for patient_data in existing_data["data"]:
                patient_id = patient_data["id"]
                allocated_time_str = patient_data["allocated_time"]

                # Convert the allocated time string to a datetime object
                allocated_time = datetime.strptime(allocated_time_str, '%Y-%m-%dT%H:%M:%S') if allocated_time_str else None
                existing_allocated_times[patient_id] = allocated_time

            # Define time constraints
            start_time = datetime.strptime("10:00", "%H:%M")
            end_time = datetime.strptime("17:00", "%H:%M")
            time_increment = timedelta(minutes=20)

            # Loop through the IDs and assign allocated time
            for i in range(0, len(existing_data["data"]), 2):
                id1 = existing_data["data"][i]["id"]
                id2 = existing_data["data"][i + 1]["id"]

                # If either ID is not in the existing_allocated_times, use start_time
                time1 = existing_allocated_times.get(id1, start_time)
                time2 = existing_allocated_times.get(id2, start_time)

                # Assign the same time for adjacent IDs
                existing_allocated_times[id1] = existing_allocated_times[id2] = time1

                # Increment time for the next two IDs
                start_time += time_increment

            # Print the resulting allocated times
            print(existing_allocated_times)

            # Make POST requests to update allocated times
            api_url_postdata = "https://digitilize-pragun.onrender.com/server3/postdata"

            for patient_id, allocated_time in existing_allocated_times.items():
                # Convert the datetime object back to a string
                allocated_time_str = allocated_time.strftime('%Y-%m-%dT%H:%M:%S') if allocated_time else None
                payload = {"id": patient_id, "allocated_time": allocated_time_str}
                response_postdata = requests.post(api_url_postdata, json=payload)
                print(response_postdata.json())

        else:
            print("Error: Response does not contain 'data' key")

    except ValueError as e:
        print(f"Error parsing JSON: {e}")
else:
    # Print an error message if the request was not successful
    print(f"Error: {response_getdata.status_code}")
