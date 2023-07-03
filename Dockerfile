# Use the official Python 3.11 image as the base
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Set up the bind mount
VOLUME /app

# Set the entrypoint to start a bash shell
CMD ["/bin/bash"]