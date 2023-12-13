from fastapi import FastAPI ,Response ,status ,HTTPException, Request
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


def print_api_response():
    api_url = "https://digitilize-pragun.onrender.com/"
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
        time.sleep(60)


# Create a background thread to run the print_api_response function
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

    cursor.execute("""SELECT * FROM login ORDER BY id DESC""")
    posts = cursor.fetchall()
    return{ "data":posts }



@app.get("/server2/getdata")
def getpost():
    cursor.execute("""SELECT * FROM patient ORDER BY id DESC""")
    posts = cursor.fetchall()
    return{ "data":posts }

@app.get("/server2/location")
def getlocation():
    cursor.execute("""SELECT "Location" FROM admin""")
    posts = cursor.fetchall()
    return{ "data":posts }

@app.get("/server2/department/{location}")
def getlocation(location :str):
    cursor.execute(f"""SELECT "Department" FROM admin WHERE "Location" LIKE '{location}'""")
    posts = cursor.fetchall()
    print (posts)
    return{ "data":posts}

@app.get("/server3/getdata")
def getpost():
    cursor.execute("""SELECT * FROM server3 ORDER BY id ASC""")
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
    cursor.execute("""INSERT INTO posts (name, age ,sex,mobile,aadhar) VALUES (%s,%s,%s,%s,%s) RETURNING *""",(
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
    # print(new)
    return{"Success":new }

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
