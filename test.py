import schedule
import time
import requests
from datetime import datetime
from datetime import datetime, timedelta
def do():
    initial = datetime.now()
    url = 'https://digitilize-pragun.onrender.com/server3/getdata'
    response = requests.get(url)
    data = response.json()

    start_time = datetime(2023, 5, 12, 9, 0)
    end_time=datetime(2023,5,12,15,0)
    appointment_duration = timedelta(minutes=30)
    appointment_time= start_time + appointment_duration

    id_1=data['data'][-1]['id']
    print(id_1)
    for j in range(0,id_1):
        for i in range(j,j+1):
            data1=data['data'][i-1]['allocatted_time']
            data1=str(data1)
            if i%2 ==0:
                appointment_time= start_time + appointment_duration
                data1 = appointment_time.strftime('%H:%M')
            else:
                data1=appointment_time.strftime('%H:%M')
            print (data1)
            

        dic={'id':i+1,'time':data1}
        print(dic)
        r=requests.post('https://digitilize-pragun.onrender.com/postdata/server3', json=dic)
        print (r.status_code)
        if r.status_code == 201:
            print('Data successfully updated')
        else:
            print('Error updating data')
        
        appointment_duration = timedelta(minutes=30)
        start_time=appointment_time



# schedule.every().day.at("01:11").do(do)  # Adjust the time as needed

# # Keep the program running to execute scheduled jobs
# while True:
#     schedule.run_pending()
#     print("hello")
#     time.sleep(1)