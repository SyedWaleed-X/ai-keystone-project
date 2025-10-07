FROM python:3.11-slim
WORKDIR /app

# Add the /app directory to Python's search path
# This is the key to making imports work easily
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copy ONLY the requirements file first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Build the Vector Store ---
# Copy everything needed to run the indexing script
COPY ./app /app/app
COPY ./data /app/data
COPY vector_store.py /app/vector_store.py

# RUN the indexing script to create the chroma_data folder
RUN python vector_store.py

# --- Final Application Setup ---
# Now that the index is built, we set up the final application.
# We will copy the app code again to the root /app directory for a clean structure.
COPY ./app .

# Expose the port and set the final run command
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]