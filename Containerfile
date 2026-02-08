FROM python:2.7-slim

WORKDIR /app

# Install Python 2.7-compatible dependencies
COPY requirements-container.txt .
RUN pip install --no-cache-dir -r requirements-container.txt

# Copy source code
COPY timesheet.py .
COPY togglapi/ togglapi/
COPY toggltime/ toggltime/

# Use config.py-example as default config (reads env vars)
COPY config.py-example config.py

# Create data directory for output
RUN mkdir -p /app/data
VOLUME /app/data

ENTRYPOINT ["python", "timesheet.py"]
