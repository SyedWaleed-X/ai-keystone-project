# Dockerfile - Final Production Version

FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pre-built vector database into the image
# THIS FAILED ON RENDER, BUT SHOULD WORK LOCALLY. WE WILL DEBUG IF IT DOESN'T.
# We are betting that the Render build environment was the problem.
COPY chroma_data ./chroma_data

# Copy the application code
COPY ./app .
    
EXPOSE 8000
# Use the $PORT variable provided by cloud hosts
CMD "uvicorn" "main:app" "--host" "0.0.0.0" "--port" ${PORT:-8000}