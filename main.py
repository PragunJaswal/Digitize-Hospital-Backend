from fastapi import FastAPI ,Response ,status ,HTTPException, Request, Path
from fastapi.params import Body          #FOR POST RESPONSE
from pydantic import BaseModel           #FOR SCHEMA
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import time
import threading
import requests
from starlette.middleware.cors import CORSMiddleware
import psycopg2                     # for databse connection
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from typing import List
import joblib


# Load the dataset
df = pd.read_csv('main.csv')
target_variable = 'prognosis'

# Split the data into features (X) and target variable (y)
X = df.drop(target_variable, axis=1)
y = df[target_variable]

# Perform one-hot encoding for categorical features
X = pd.get_dummies(X)

# Encode the target variable
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)



app =FastAPI()

origins = [
    "https://digitilize-pragun.onrender.com/getdata",
    "http://digitilize-pragun.onrender.com/getdata",
    "http://digitilize-pragun.onrender.com",
    "http://localhost",
    "http://localhost:8080",
]



my_post= [
    {"name":"Jaswal","age":"45","sex":"Male","mobile":8544722770,"aadhar":78415162770,"id":1},
    {"name":"rahul","age":"25","sex":"female","mobile":9459770218,"aadhar":9985544722770,"id":2}
    ]


#                                       Schema class for post
class Post(BaseModel):
    name: str = "test"   #test is default if not filled
    age: int
    sex: str
    mobile: int
    aadhar: int

                            #Server 2 Schema
class Post2(BaseModel):
    name: str  
    age: int
    sex: str
    location: str
    department: str
    date: str
    time: str

class Post3(BaseModel):
    id: int
    allocated_time: str

class Post4(BaseModel):
    id:int
    reason: str
    available_in: str

class SymptomsInput(BaseModel):
    symptoms: List[str]

                    #connection with database
while True:
    try:
        conn = psycopg2.connect(host = 'db.idojuihasgaurthhrddn.supabase.co', database ='postgres', 
                            user='postgres' ,password ='PragunJaswal',cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("DATABASE CONNECTED")
        break

    except Exception as error:
        print("Connection is not Establised")
        print("Error was ",error)
        time.sleep(2)

templates =Jinja2Templates(directory="templates")
        

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host='db.idojuihasgaurthhrddn.supabase.co',
            database='postgres',
            user='postgres',
            password='PragunJaswal',
            cursor_factory=RealDictCursor
        )
        print("DATABASE CONNECTED")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_database_connection(conn):
    if conn:
        conn.close()
        print("DATABASE CONNECTION CLOSED")

database_connection = connect_to_database()

if database_connection:
    try:
        # Your database operations here
        cursor = database_connection.cursor()
        cursor.execute("SELECT * FROM login ORDER BY id")
        result = cursor.fetchall()
        print("Database Query Result:", result)
    except psycopg2.Error as e:
        print(f"Error executing database query: {e}")
        # Close and restart the connection if needed
        close_database_connection(database_connection)
        database_connection = connect_to_database()
else:
    print("Database connection not established. Cannot perform database operations.")

def print_api_response():
    api_url = "https://digitilize-pragun.onrender.com/getdata"
    while True:
    
        try:
            # Make a GET request to the API
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the API response content
                print(response.text)
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Wait for 60 seconds before making the next request
        time.sleep(61)


# Create a background thread to run the print_api_response function:
background_thread = threading.Thread(target=print_api_response)


@app.get("/gettable", response_class=HTMLResponse)
def gettable(request : Request):
    return templates.TemplateResponse("index.html",{"request": request} )


@app.get("/server2/gettable", response_class=HTMLResponse)
def gettable(request : Request):
    return templates.TemplateResponse("server.html",{"request": request} )


@app.get("/")
def root():
    return{"server is running"}

@app.get("/test")
def root():
    return{"server is running but database might be is down ;("}


@app.get("/getdata")
def getpost():
    try:
            # Make a GET request to the API
        cursor.execute("""SELECT * FROM login ORDER BY id DESC""")
        posts = cursor.fetchall()
        return{ "data":posts }
    except Exception as e:
        close_database_connection(database_connection)
        database_connection = connect_to_database()
        print(f"An error occurred given as: {str(e)}")
        return(f"error exsisted as {e}")
        


@app.get("/getadmin")
def getpost():
    cursor.execute("""SELECT * FROM admin_login ORDER BY id DESC""")
    posts = cursor.fetchall()
    return{ "data":posts }

@app.get("/get/status/doctor")
def getpost():
    cursor.execute("""SELECT * FROM doctors ORDER BY id DESC""")
    posts = cursor.fetchall()
    return{ "data":posts }


@app.get("/update/doctor/{registration_id}")
def update_doctor_status(registration_id: int,state: int = 0):
    cursor.execute(f"""UPDATE public.doctors SET status = {state} WHERE registration_id = {registration_id}""")
    conn.commit()
    conn.rollback()
    return {"updated"}

@app.get("/server2/getdata")
def getpost():
    cursor.execute("""SELECT * FROM patient ORDER BY age DESC""")
    posts = cursor.fetchall()
    return{ "data":posts }
# 
@app.get("/server2/location")
def getlocation():
    cursor.execute("""SELECT DISTINCT "Location" FROM admin""")
    posts = cursor.fetchall()
    return{ "data":posts }

# @app.get("/server2/parchi")
# def getlocation():
#     cursor.execute("""SELECT DISTINCT "Location" FROM admin""")
#     posts = cursor.fetchall()
#     return{ "data":posts }
 
@app.get("/server2/department/{location}")
def getlocation(location :str):
    cursor.execute(f"""SELECT "Department" FROM admin WHERE "Location" LIKE '{location}'""")
    posts = cursor.fetchall()
    print (posts)
    return{ "data":posts}

@app.get("/server3/getdata")
def getpost():
    cursor.execute("""SELECT * FROM patient ORDER BY id ASC""")
    posts = cursor.fetchall()
    return{ "data":posts }

@app.get("/getsymptoms")
def get_symptoms():
    symptoms = [
        'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
        'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
        'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings',
        'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever',
        'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin',
        'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation',
        'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure',
        'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
        'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain',
        'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
        'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
        'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremities',
        'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain',
        'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness',
        'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell',
        'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases',
        'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium',
        'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes',
        'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration',
        'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma',
        'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum',
        'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurrying',
        'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
        'red_sore_around_nose', 'yellow_crust_ooze'
    ]

    return [{"symptoms": symptoms}]



@app.get("/get/status/doctor/{registration_id}")
def getpost(registration_id: int):
    cursor.execute(f"""SELECT * FROM doctors WHERE registration_id = {registration_id}""")
    posts = cursor.fetchall()
    return{ "data":posts }

@app.post("/post/status/doctor/")
def update_Status(payload: Post4):
    try:
        with conn.cursor() as cursor:
            query = """UPDATE public.doctors SET reason = %s ,available_in = %s WHERE id = %s"""
            cursor.execute(query, (payload.reason,payload.available_in,payload.id))
            # Commit the changes to the database
            conn.commit()
        return {"message": f"Updated {payload.id}"}
    except Exception as e:
        # If there's an error, rollback the changes
        conn.rollback()
        # Optionally, raise an HTTP exception with the error details
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/server3/postdata",status_code=201)
def post_time(payload: Post3):
    allocated_time = datetime.strptime(payload.allocated_time, '%Y-%m-%d %H:%M:%S')
    formatted_allocated_time = allocated_time.strftime(r'%Y-%m-%d %H:%M:%S')
    print(formatted_allocated_time,payload.id)
    try:
        with conn.cursor() as cursor:
            query = """UPDATE public.patient SET allocated_time = (TIMESTAMP %s) WHERE id = %s"""
            cursor.execute(query, (formatted_allocated_time, payload.id))
            # Commit the changes to the database
            conn.commit()
        return {"message": f"Allocated time updated for patient ID {payload.id}"}
    except Exception as e:
        # If there's an error, rollback the changes
        conn.rollback()
        # Optionally, raise an HTTP exception with the error details
        raise HTTPException(status_code=500, detail=str(e))
    # cursor.execute("""UPDATE public.patient SET allocated_time = %s  WHERE id = %s""",formatted_allocated_time,payload.id)
    # new =cursor.fetchone()
    # conn.commit()
    # conn.rollback()
    # return{ "data"} 



@app.post("/post")                          # simple post
def post(payload: dict = Body(...)):
    print(payload)
    return{f"{payload} success"}
 
                                            #Post with schema

@app.post("/postdata",status_code=201)        #DEFAULT RESPONSE 201
def post(payload: Post):
    # print(payload.name)         print  a specific key data
    # payload.dict()              #convert class of schema to dictanory datatype
    # new = payload.dict()
    # new['id']=randrange(0,100000)
    # my_post.append(new)
    cursor.execute("""INSERT INTO login (name, age ,sex,mobile,aadhar) VALUES (%s,%s,%s,%s,%s) RETURNING *""",(
    payload.name,payload.age,payload.sex,payload.mobile,payload.aadhar))
    new =cursor.fetchone()
    conn.commit()
    conn.rollback()
    return{"Success":new }


@app.post("/server2/postdata",status_code=201)        #DEFAULT RESPONSE 201
def post(payload: Post2):
    cursor.execute("""INSERT INTO patient (name, age ,sex,location,department,date,time) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *""",(
            payload.name,payload.age,payload.sex,payload.location,payload.department,payload.date,payload.time))
    new =cursor.fetchone()
    conn.commit()
    conn.rollback()
    # conn.rollback()
    # print(new)
    return{"Success":new }


@app.post("/predict/deptt")
# Now, let's make predictions for a user with symptoms using the saved model
def model (symptoms_input: SymptomsInput):
    loaded_model = joblib.load('main.pkl')

    user_symptoms = ['itching','skin_rash','nodal_skin_eruptions']
    user_data = pd.DataFrame(index=[0], columns=X.columns)
    user_data[:] = 0
    user_data.loc[:, symptoms_input.symptoms] = 1

    # Predict the disease for the user using the loaded model
    predictions_nb = loaded_model.predict(user_data)
    probability_nb = loaded_model.predict_proba(user_data)[:, 1]
    predicted_disease_nb = label_encoder.inverse_transform(predictions_nb)

    # print(f"Predicted Disease (Naive Bayes): {predicted_disease_nb[0]}")
    formatted_probability = float(probability_nb * 1000)  
    print(f"Probability Estimate (Naive Bayes): {formatted_probability}")

    if formatted_probability <= 200:
        Predicted_deptt = "GENERAL"
    else:
        Predicted_deptt = predicted_disease_nb[0]

    return{"Department":Predicted_deptt}
    




#                                           get a item with id

def find(id):
    for i in my_post:
        if i["id"] == id:
            return i



@app.get("/getdata/{id}")
def getid(id : int , response : Response):
    # data = find(int(id))
    print(id)
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id} """)
    new = cursor.fetchone()
    
    if not new:                             #METHOD TO THROUGH RESPONSE WHEN NO ID IS MATCHED

        raise HTTPException(status_code=404 , detail="Not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"Message":f"id:{id} not found"}
    return{"data":f"requested data {new}"}


@app.get("/getbymobile/{mobile}")
def getbymobile(mobile : int , response : Response):
    # data = find(int(id))
    cursor.execute(f"""SELECT * FROM login WHERE mobile = {mobile} """)
    new = cursor.fetchone()
    
    if not new:                             #METHOD TO THROUGH RESPONSE WHEN NO ID IS MATCHED

        raise HTTPException(status_code=404 , detail="Data not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"Message":f"id:{id} not found"}
    return{"data":new}




#                                       logic to get latest post
@app.get("/getlatest")
def latest():
    post = my_post[len(my_post)-1]
    return {"data":post}



def delete(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i



@app.delete("/delete/{id}")
def delete_post(id : int):
    index =delete(id)

    if index == None:
        raise HTTPException(status_code=404, detail="Not Found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




                                         #update the post


@app.put("/post/{id}")
def update(id: int ,post: Post):
    index =delete(id)

    if index == None:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        postdict = post.dict()
        postdict['id'] = id
        my_post[index] =postdict


    return{"data":my_post}

app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)
