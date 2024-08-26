# Use an official Python runtime as a parent image
FROM python:3.12.4

# Set the working directory in the container
# where all my files are
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# cache the requirements
COPY ./requirements.txt /app
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# copy all scripts to the folder
COPY . /app

# Define environment variable
ENV NAME=hms-venv

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]