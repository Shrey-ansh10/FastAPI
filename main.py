from fastapi import FastAPI, Path, HTTPException, Query
import json
# import patients.json

app = FastAPI() #creating app instance of FastAPI that will run on server

# a function that loads data and return data to whoever called it - a utility function
def load_data():
    with open('patients.json', "r") as f:
        data = json.load(f)
    return data


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

