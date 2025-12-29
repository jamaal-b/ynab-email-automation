FROM python:3.11-slim

# Set UTF-8 encoding
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make main.py executable
RUN chmod +x main.py

# Run the scheduler
CMD ["python", "-u", "main.py"]
