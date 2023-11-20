FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.presentation.api.v1.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]