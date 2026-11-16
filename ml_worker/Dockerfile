FROM autogluon/autogluon:1.3.1-cpu-framework-ubuntu22.04-py3.11

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/AutogluonModels

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ml_service.py .

EXPOSE 8001

CMD ["uvicorn", "ml_service:app", "--host", "0.0.0.0", "--port", "8001"]
