FROM python:3.10-slim

# Install Chrome & dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 \
    libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    xdg-utils libu2f-udev \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install ./google-chrome-stable_current_amd64.deb -y && \
    rm google-chrome-stable_current_amd64.deb

# Set display port to avoid crash
ENV DISPLAY=:99

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy code
COPY . .

CMD ["python", "main.py"]
