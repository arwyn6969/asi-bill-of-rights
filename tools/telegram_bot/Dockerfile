FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (coincurve might need build-essential)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy root requirements.txt (it's at the project root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to /app
COPY . .

# Set environment
ENV PYTHONPATH=.
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python3", "tools/telegram_bot/kevin_bot.py"]
