# FastAPI

Made using Starlette and Pydantic.
-> Starlette : manages how API requests are sent and received
-> Pydantic : for validating if the data received and send in correct format or not.

Philosophy: 
- Provides Fast running api - mitigating the drawback of other frameworks
- The API creation will be fast to write as well.

Why fast to run?
- Fast API is able to achieve this fastness, because of the components it user. These components allow asynchronous operations.
    - Uvcorn : web server - provide low latency and multiple request serving capabilities 
    - Async standard gateway interface (asgi) : converts HTTP requests to parsable data - also asynchronous 
    - Python code we write is also asynchronous 

Why fast to code?
- Provides automatic input validation
- Auto generated interactive documentation
- Seamless integration with modern AI/ML libraries, OAuth, docker, Kubernetes, SQL Alchemy, etc.


Project Setup Steps:
1. Create a directory - fastapi-apps
2. "uv init" [install uv if it's not installed]
3. "uv venv" - create a virtual environment
4. uv add "fastapi[standard]" - installs fastapi and it's related packages
create api end points in main
5. "uvicorn main:app --reload" -> starts the server on local host

# 4 main Operations we do:
1. Create - to create new records
2. Read - to retrieve and read data
3. Update - to change/update data
4. Delete - to delete record/data

## PATH PARAMETERS:  
- Parameters that are retrieved from URL and is used to get specific data
Eg: In our case, we create a endpoint that the user can hit with a specific patient id and we will retrieve and return patients records accordingly.

- Path() : It's a function in fastapi that's used to provides *Metadata*, *Validation Rules*, and *Documentation Hints* for path parameters in API end points.


## Query parameter
- Optional key-value pair appended to the end of the url, used to pass additional data with the HTTP request.
- Used for operations like sorting, searching, filtering, etc; without altering the API endpoint.
- "?" marks the start of the query
- each pair is a key-value pair -> key=value
- multiple parameters are seperated by "&"
e.g. /patient?city=delhi&sort_by=age (not mandatory for all key-value pair to be in lower case)

- Query() : a function provided by fastapi to declare, validate and document query parameters
- It allows to set: 1. default value  2. add validation rule 3. add metadata like description, title, examples



------------------------------------------------------------

## CREATE Operation using PUT method.

- Allow a patient to update his records. 

    For this:
    1. We will create a new patient model using pydantic, making the fields as optional, single or multiple fields can be updated, as required.

    2. create the PUT endpoint where we accept data from the client and update record of that patient.

## DELETE operation using DELETE method
- Deleting existing records.
