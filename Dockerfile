# 1. Start from an official lightweight Python base image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application files into the container
# This includes main.py and model.joblib
COPY . .

# 5. Command to run the application when the container starts
# This tells uvicorn to run the 'app' instance from the 'main.py' file
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]