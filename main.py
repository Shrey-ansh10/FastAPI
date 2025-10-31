from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI() #creating app instance of FastAPI that will run on server

# a function that loads data and return data to whoever called it - a utility function
def load_data():
    with open('patients.json', "r") as f:
        data = json.load(f) 
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# creating a simple get end point - like home page
@app.get("/")
def hello():
    return "Hello from the ADMIN. This is a API for patients management."

@app.get("/about")
def about():
    return "This is a functional API for patient management. He he he."

# VIEW  end point will return all the data we have in patients.json
@app.get("/view")
def view():
    data = load_data()
    return data

# PATIENTS endpoint : a end point that will return some specific data - can be used to retrive specific data
@app.get("/patient/{patient_id}") # patient_id is the path parameter
def get_patient(patient_id: str = Path(..., description = "Pass in ID of Patient. It should be in string format and look like the example below.", example = "P0000", )): # call the path function here itself and add params in it | ... states the parameter is necessary
    data = load_data()
    if patient_id in data.keys():
        return data.get(patient_id)
    # return "Data not found. This Patient ID might not exist."
    raise HTTPException(status_code=404, detail="patient not found")


# sort endpoint and implement query parameters 
@app.get("/sort")
def sort(sort_by:str = Query(..., description="sort by height, weight, umar"), order:str = Query('asc', description="order of sorting. Set to ascending by default.")):
    
    # putting check on the query params
    if sort_by not in ["height", "weight", "umar"]:
        raise HTTPException(status_code=400, detail='Invalid field. give height, weight, umar')
    
    if order not in ["asc", "des"]:
        raise HTTPException(status_code=400, detail="Can only sort in ascending ot decending order.")
    
    data = load_data() #loading data

    sort_order = True if order == "asc" else False # defining sort value 
    # if(order=="asc"): sort_order = True
    # else: sort_order = False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data # return statement is very necessary in the function

# ------- All the above endpoints were sending data to the client's GET request
# ------- Next we will create a POST endpoint where the client can send some data to server


# ---- First, we'll create a data model using pydantic as follow
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Literal
from fastapi.responses import JSONResponse

class Patient(BaseModel):
    name : Annotated[str, Field(..., description="enter patient name")]
    pitaji_name : Annotated[str, Field(..., description="enter patient's pitaji's name")]
    umar : Annotated[int, Field(..., gt=16, lt=100, description="Enter age")]
    gender : Annotated[Literal["male", "female", ], Field(...,description="enter the gender of patient.")]
    height : Annotated[float, Field(...,gt=0, lt=3, description="enter height in meters")]
    weight : Annotated[float, Field(...,gt=25, lt=300, description="Weight values must me btw 25 and 300")]


# Now creating a post endpoint where the client can send the data.

@app.post("/create_patient")
def create_patient(patient:Patient): # the data that is sent by client to server, will be validated throught the 

    #load data
    data = load_data()

    #create a new ID for patient
    # out patient id looks like -> P0001 - P followed by 4 digits - so we willhave to extract digits, increment by 1 and then appent it back with P

    existing_ids = data.keys() # extracting current patient ids
    if not existing_ids: #if there is no patient id, start with 1
        next_num = 1
    else:
        # extract number from existing id and pull out the max from it
        current_max = max(int(pid.replace('P','')) for pid in existing_ids) #removing P and extracting digits
        next_num = current_max+1 #incrementing by 1

    patient_id = f"P{next_num:04d}" #appending incremented value with P

    #append the data to the data base
    data[patient_id] = patient.model_dump()

    save_data(data) # a function for saving data to the data base

    return JSONResponse(status_code=200, content=f"{patient}")

# That wraps our post endpoints - but it's not good endpoint, because the client might send same data and create 100s of patients with same record.
# This is a critical bug 
# To be handles it few things can be done
# 1. Creating a hash function - but it's pretty technical and beyond the scope of api development - but a software engineer like me can help 
# 2. By checking if name already exists in the data base, then check father's name then check age, if after 3 passes the data is still same, reject that data and respond the data already exist.
