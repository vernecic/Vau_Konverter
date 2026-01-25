FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

ENV PIP_PROGRESS_BAR=off
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]

