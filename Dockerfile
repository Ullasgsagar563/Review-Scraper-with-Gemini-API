# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy contents of the current directory to /app in the container
COPY . /app

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    libgconf-2-4 \
    libnss3 \
    libx11-xcb1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libasound2 \
    libxshmfence1 \
    libxss1 \
    wget \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browser dependencies
RUN pip install playwright && playwright install --with-deps

# Expose ports for both services
EXPOSE 8000 8501

# Command to run both services (Backend and Frontend)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
