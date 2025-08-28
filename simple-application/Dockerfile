FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=production
EXPOSE 9000
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "app:app", "--workers", "2"]
