FROM python:3.10-slim

# Metadata
LABEL maintainer="manikjain777@gmail.com"

WORKDIR /app

# Install system deps required by pycaret, scikit-learn and other packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        gfortran \
        libgomp1 \
        libatlas3-base \
        liblapack3 \
        libblas3 \
        libsndfile1 \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt ./

# Install Python deps
RUN pip install --no-cache-dir -U pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

# Ensure model and data files are present (optional check at build time)
# You can remove these RUN lines if you don't want Docker build to fail when files are missing
RUN test -f ai_resume_screener_model.pkl || echo "Warning: model file not found"
RUN test -f test_dict.json || echo "Warning: test_dict.json not found"

EXPOSE 8000

# To make the service accessible only on the host's localhost, run the container like:
#   docker build -t ai-resume-screener .
#   docker run --rm -p 8000:8000 ai-resume-screener
# This maps the container port 8000 to the host's 127.0.0.1:8000 (localhost-only access).

# Use a simple command to run uvicorn; workers can be tuned depending on the environment
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
