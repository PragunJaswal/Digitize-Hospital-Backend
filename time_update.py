import requests

# Make the API request
api_url = "https://digitilize-pragun.onrender.com/server3/getdata"
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Process the data and create the dictionary
    id_allocated_time_dict = {}

    for patient_data in data["data"]:
        patient_id = patient_data["id"]
        allocated_time = patient_data["allocated_time"]

        # Add to the dictionary, set to 0 or None if allocated_time is null
        id_allocated_time_dict[patient_id] = allocated_time if allocated_time is not None else None

    # Print the resulting dictionary
    print(id_allocated_time_dict)

else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code}")
