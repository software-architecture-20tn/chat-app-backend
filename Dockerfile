# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
  pip install -r requirements/development.txt

# Expose port 8000 for the Django application
EXPOSE 8000

# Start the application using gunicorn (adjust the command as needed)
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myapp.wsgi:application"]
