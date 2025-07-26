# Dockerfile (Corrected Version 2)

# --- Stage 1: Builder ---
# We use a "slim" Python image to install dependencies
# FIX 1: Changed 'as' to 'AS' to resolve the casing warning.
FROM python:3.11-slim AS builder

# Define the working directory inside the container
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Image ---
# Start again from a clean image to keep the final size small
FROM python:3.11-slim

WORKDIR /app

# Copy the entire Python installation path from the builder,
# which includes both the libraries (site-packages) and the executables (bin).
COPY --from=builder /usr/local/ /usr/local/

# Copy the entire application code into the container
COPY . .

# Expose port 8000, the default port for our FastAPI/Uvicorn server
EXPOSE 8000

# FIX 2: Changed "api_main.py:app" to "api_main:app".
# This tells Uvicorn to import the module 'api_main' and find the object 'app' inside it.
CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
