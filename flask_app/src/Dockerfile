FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY main ./main/
COPY setup.py .
COPY MANIFEST.in .

# Install the package directly with pip using setup.py
RUN pip install --no-cache-dir -e .

# Verify installation
RUN python -c "import app; print('✓ App installed successfully')" && \
    python -c "import app, os; app_dir = os.path.dirname(app.__file__); print('App location:', app_dir)" && \
    python -c "import app, os; assert os.path.exists(os.path.join(os.path.dirname(app.__file__), 'templates')), 'Templates folder missing!'; print('✓ Templates folder found')" && \
    python -c "import app, os; assert os.path.exists(os.path.join(os.path.dirname(app.__file__), 'static')), 'Static folder missing!'; print('✓ Static folder found')"

# Expose Flask port
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PYTHONUNBUFFERED=1

# Start Flask
CMD ["flask", "run"]
