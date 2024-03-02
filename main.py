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
df = pd.read_csv('aabb.csv')
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
    available_in: int

class SymptomsInput(BaseModel):
    symptoms: List[str]

                    #connection with database
while True:
    try:
        conn = psycopg2.connect(host = 'aws-0-ap-south-1.pooler.supabase.com', database ='postgres', 
                            user='postgres.idojuihasgaurthhrddn' ,password ='PragunJaswal',cursor_factory= RealDictCursor)
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
            host='aws-0-ap-south-1.pooler.supabase.com',
            database='postgres',
            user='postgres.idojuihasgaurthhrddn',
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
    cursor.execute("""SELECT * FROM patient ORDER BY id DESC""")
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
    cursor.execute("""SELECT * FROM patient ORDER BY age DESC""")
    posts = cursor.fetchall()
    return{ "data":posts }

@app.get("/getsymptoms")
def get_symptoms():
    symptoms = [
        'itching','skin_rash', 'nodal_skin_eruptions','continuous_sneezing','shivering','chills',
                'joint_pain','stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition',
                'spotting_ urination','fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss',
                'restlessness','lethargy','patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes',
                'breathlessness','sweating','dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea',
                'loss_of_appetite','pain_behind_the_eye','back_pain','constipation','abdominal_pain','diarrhoea','mild_fever'
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

@app.get("/get/previous/patient/{mobile_num}")
def getpost(mobile_num: int):
    cursor.execute(f"""SELECT * FROM public.patient where mobile_num = {mobile_num}""")
    posts = cursor.fetchall()
    return{ "data":posts }



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

class SymptomInput(BaseModel):
    symptoms: List[str]

import csv
def get_suggestion(symptom):
    with open('suggestion1.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Symptom'].lower() == symptom.lower():
                return row['Home Care Suggestions']
    return f"Suggestion not found for symptom: {symptom}"

@app.post("/get_home_care_suggestions")
async def get_home_care_suggestions(symptom_input: SymptomInput):
    suggestions = {}
    for symptom in symptom_input.symptoms:
        suggestions[symptom] = get_suggestion(symptom)
    return {"home_care_suggestions": suggestions}



schemes=  {
    "Nikshay Poshan Yojana":"Ministry of Health and Family Welfare, Government of India has announced the scheme for incentives for nutritional support to TB patients. This scheme will be called “Nikshay Poshan Yojana”.",
 "Nikshay Poshan Yojana (Nutritional Support To TB Patients)":"An incentive scheme under National Health Mission (NHM) by Central TB Division of MoHFW for Tuberculosis (TB) patients who are under treatment and have registered / notified themselves on the NIKSHAY portal. The incentives can be distributed in Cash or in Kind.",
 "Rastriya Arogya Nidhi - Health Minister's Cancer Patient Fund":"A scheme to provide financial assistance to poor patients living below poverty line and suffering from cancer, for their treatment at 27 Regional cancer centers (RCCs).",
 "National AIDS Control Organisation (NACO) Programme":"NACO initiated the Internship Programme for young students who wish to engage with the Government. The internship programme envisages an opportunity for young students to get familiar with and understand the various dimensions of policy-making & implementation of the National AIDS",
 "Short Term Fellowship under the Human Resource Development Programme for Health Research":"Short Term Fellowship under the Human Resource Development Programme for Health Research aims to provide advanced training in India & abroad to medical and health research personnel in cutting-edge research areas related to medicine & health.",
 "Long Term Fellowship under the Human Resource Development Programme for Health Research":"Long Term Fellowship under the Human Resource Development Programme for Health Research aims to provide advanced training in India and abroad to medical and health research personnel in cutting-edge research areas related to medicine and health.",
 "Health Minister's Discretionary Grant":"A health scheme by Ministry of Health & Family Welfare for financially poor patients to defray a part of the expenditure on Hospitalization/treatment in Government Hospitals,for life threatening diseases covered under Rashtriya Arogya Nidhi (RAN), in cases where free medical facilities aren't there.",
    }


@app.get("/get/govt/schemes")
def getschemes():

    return{"data": schemes}

@app.post("/predict/deptt")
# Now, let's make predictions for a user with symptoms using the saved model
def model (symptoms_input: SymptomsInput):
    loaded_model = joblib.load('finalm.pkl')
    
    user_data = pd.DataFrame(index=[0], columns=X.columns)
    user_data[:] = 0
    user_data.loc[:, symptoms_input.symptoms] = 1

# Predict the probability for the predicted department using Random Forest
    predicted_probs_rf = loaded_model.predict_proba(user_data)[0]
    predicted_dept_rf = label_encoder.inverse_transform(loaded_model.predict(user_data))[0]

# Extract the probability for the predicted department
    probability_estimate = predicted_probs_rf[label_encoder.transform([predicted_dept_rf])[0]]

    # print(f"Predicted Disease (Naive Bayes): {predicted_disease_nb[0]}")
# Check if the probability estimate is 0.0 and assign "General" in that case
    if probability_estimate == 0.0:
        predicted_dept_rf = "General"

    print(f"Probability Estimate: {probability_estimate}")
    return{"Department":predicted_dept_rf}

#     if formatted_probability <= 200:
#         Predicted_deptt = "GENERAL"
#     else:
#         Predicted_deptt = predicted_disease_nb[0]

#     return{"Department":Predicted_deptt}
    
# # Now, let's make predictions for a user with symptoms using the saved model
# loaded_model = joblib.load('main.pkl')

# user_symptoms = ['back_pain']
# user_data = pd.DataFrame(index=[0], columns=X.columns)
# user_data[:] = 0
# user_data.loc[:, user_symptoms] = 1

# # Predict the probability for the predicted department using Random Forest
# predicted_probs_rf = loaded_model.predict_proba(user_data)[0]
# predicted_dept_rf = label_encoder.inverse_transform(loaded_model.predict(user_data))[0]

# # Extract the probability for the predicted department
# probability_estimate = predicted_probs_rf[label_encoder.transform([predicted_dept_rf])[0]]

# # Check if the probability estimate is 0.0 and assign "General" in that case
# if probability_estimate == 0.0:
#     predicted_dept_rf = "General"

# print(f"Department (Random Forest): {predicted_dept_rf}")
# print(f"Probability Estimate: {probability_estimate}")



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
