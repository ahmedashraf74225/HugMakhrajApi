FROM python:3.9

# Set up environment variables
ENV TRANSFORMERS_CACHE=/cache/huggingface/hub

# Create cache directory and set permissions
RUN mkdir -p /cache/huggingface/hub && \
    chmod -R 777 /cache

# Set working directory
WORKDIR /code

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
