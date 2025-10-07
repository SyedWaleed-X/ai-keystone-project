# Dockerfile (Simplest Possible Version)
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy EVERYTHING from your local project into the container
COPY . .

# Run the indexing script, which is now at /app/vector_store.py
RUN python vector_store.py

EXPOSE 8000
# The CMD now needs to point to app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]