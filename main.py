from fastapi import FastAPI ,Response ,status ,HTTPException, Request
from fastapi.params import Body          #FOR POST RESPONSE
from pydantic import BaseModel           #FOR SCHEMA
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


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

app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)


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


                    #connection with database
while True:
    try:
        conn = psycopg2.connect(host = 'dpg-ch2kh3t269v61fdprae0-a.singapore-postgres.render.com', database ='database_acqv', 
                            user='pragun' ,password ='GSwaaOpWxmCEposCnIO4QUayDizDgffY',cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("DATABASE CONNECTED")
        break

    except Exception as error:
        print("Connection is not Establised")
        print("Error was ",error)
        time.sleep(2)

templates =Jinja2Templates(directory="templates")


@app.get("/gettable", response_class=HTMLResponse)
def gettable(request : Request):
    return templates.TemplateResponse("index.html",{"request": request} )


@app.get("/")
def root():
    return{"server is running"}

@app.get("/getdata")
def getpost():
    cursor.execute("""SELECT * FROM posts""")
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
    return{"data":f"here is the requested data {new}"}


@app.get("/getbymobile/{mobile}")
def getbymobile(mobile : int , response : Response):
    # data = find(int(id))
    cursor.execute(f"""SELECT * FROM posts WHERE mobile = {mobile} """)
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




