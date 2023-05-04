FROM python:3.11

# Keeps Python from generating .pyc files in the container 
ENV PYTHONDONTWRITEBYTECODE=1 

# Turns off buffering for easier container logging 
ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || (echo "Failed to install dependencies" && exit 1)


COPY / app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
