FROM python:3.11-slim

# system dependencies for PyMuPDF, poppler, etc.
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    mupdf-tools \
    poppler-utils \
    libmagic1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . .

# download NLTK dependencies
RUN python -m nltk.downloader punkt

# Expose Django port
EXPOSE 8000

CMD ["gunicorn", "plagiarism.wsgi:application", "--bind", "0.0.0.0:8000"]
