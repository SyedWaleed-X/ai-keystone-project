# Dockerfile

# Step 1: Start with a lean base image.
FROM python:3.11-slim

# Step 2: Set the working directory inside the container.
WORKDIR /app

# Step 3: Set the PYTHONPATH environment variable.
# This helps Python find your modules (like 'app.embedder') without issues.
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Step 4: Copy ONLY the requirements file for optimal caching.
COPY requirements.txt .

# Step 5: Install all Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy your application's logic.
# This copies your 'app' folder into '/app/app' inside the container.
COPY ./app /app/app

# Step 7: Copy your PRE-BUILT data asset.
# This is the key. We are copying the 'chroma_data' folder that you
# just rebuilt with the new model.
COPY ./chroma_data /app/chroma_data

# Step 8: Expose the port the application will run on.
EXPOSE 8000

# Step 9: Define the final command to start the API server.
# This command runs when the container starts.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]