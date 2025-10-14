# The Final, Lean, "Pre-Built Index" Dockerfile

FROM python:3.11-slim
WORKDIR /app

COPY requirements_backend.txt ./requirements.txt
# This RUN layer will be cached and fast after the first build
RUN pip install --no-cache-dir -r requirements.txt

# This COPY command is now the key. It copies the pre-built index.
COPY chroma_data ./chroma_data

# This copies your application code.
COPY ./app .
    
EXPOSE 8000
# Use the $PORT variable from Render, default to 8000
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}