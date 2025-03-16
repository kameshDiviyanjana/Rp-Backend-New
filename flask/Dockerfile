# FROM python:3.12.3
# WORKDIR /app
# COPY requiment.txt ./
# RUN pip install -r requiment.txt
# COPY . .
# CMD ["python", "app.py"]
# EXPOSE 5000
FROM python:3.11

WORKDIR /app

# Copy requirements.txt to the container and install the dependencies
COPY requiment.txt ./
RUN pip install --upgrade pip && pip install -r requiment.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 (flask default port)
EXPOSE 5000

# Command to run the application
CMD ["python", "api.py"]
