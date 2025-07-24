FROM python:3.10-slim

# Install Chrome & dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 \
    libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    xdg-utils libu2f-udev \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome properly
RUN apt-get update && \
    apt-get install -y wget gnupg2 curl && \
    curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Set display env (for headless Chrome)
ENV DISPLAY=:99

# Copy your project files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your script
CMD ["python", "main.py"]

