FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || (echo "Failed to install dependencies" && exit 1)


COPY / app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
