FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Keeps Python from generating .pyc files in the container 
ENV PYTHONDONTWRITEBYTECODE=1 
 
# Turns off buffering for easier container logging 
ENV PYTHONUNBUFFERED=1 

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt || (echo "Failed to install dependencies" && exit 1)

# Create a non root user to access the container 
RUN id -u vscode &>/dev/null || adduser -u 5678 --disabled-password --gecos "" vscode