# Use the official Python base image
FROM python:3.9.20-alpine3.20

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# Install ssh
RUN \
    apk add --no-cache openssh-client

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8002

# Run the FastAPI application using uvicorn server
CMD ["python3", "main.py"]