#setup python version
FROM python:3.10-slim

#select working directory
WORKDIR /app

#copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

#copy rest of the application code
COPY . .

#expose port
EXPOSE 8000

# to run server 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]