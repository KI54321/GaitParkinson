# Use an official Python runtime as the parent image
FROM python:3.8

# Set environment variables to ensure that Python outputs everything that's printed inside
# the application rather than buffering it
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN pip install --no-cache-dir Flask firebase_admin joblib pandas scikit-learn

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run server.py when the container launches
CMD ["python", "server.py"]
