FROM python:3.11-slim

WORKDIR /app

# Add system dependencies for Open3D
RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-6 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
