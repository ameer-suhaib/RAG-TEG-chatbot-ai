FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]


#use python 3.13
#create work dir app
#copy requirements.txt file
#Copies your project
#Starts FastAPI with Uvicorn