# Use the official Python 3.11 image as the base image
FROM python:3.11

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./requirements.txt /app/requirements.txt

# Install Python libraries
RUN pip install --no-cache-dir --no-dependencies -r /app/requirements.txt

# Copy the local 'asr' directory into the container
COPY ./asr /app/asr

# Expose port 8001 for external access to the container
EXPOSE 8001

# Disable CUDA by making GPUs invisible to PyTorch or other libraries
ENV CUDA_VISIBLE_DEVICES=""

# Run the ASR API script when the container starts
CMD ["python", "/app/asr/asr_api.py"]