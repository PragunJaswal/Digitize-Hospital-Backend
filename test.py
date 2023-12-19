# import schedule
import requests
from datetime import datetime, timedelta

def do():
    url = 'https://digitilize-pragun.onrender.com/server3/getdata'
    response = requests.get(url)
    data = response.json()

    start_time = datetime(2023, 5, 12, 9, 0)
    appointment_duration = timedelta(minutes=30)

    for patient_data in data["data"]:
        patient_id = patient_data["id"]

        if patient_id % 2 == 1:
            # For odd IDs, update the allocated time
            patient_data["allocated_time"] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            start_time += appointment_duration

    # Update the existing data on the server
    update_url = 'https://digitilize-pragun.onrender.com/server3/postdata'
    update_data = {"data": data["data"]}
    update_response = requests.post(update_url, json=update_data)

    if update_response.status_code == 201:
        print('Data successfully updated')
    else:
        print(f'Error updating data. Status code: {update_response.status_code}')

do()
# schedule.every().day.at("01:11").do(do)  # Adjust the time as needed

# # Keep the program running to execute scheduled jobs
# while True:
#     schedule.run_pending()
#     print("hello")
#     time.sleep(1)