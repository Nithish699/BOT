FROM python:3.10-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 fonts-liberation libappindicator3-1 \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libu2f-udev ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download and install Chrome manually
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y /tmp/chrome.deb && \
    rm /tmp/chrome.deb

# Install matching chromedriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+\.\d+" | cut -d '.' -f 1) && \
    DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Set display env (headless chrome support)
ENV DISPLAY=:99

# Copy code
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run script
CMD ["python", "main.py"]
