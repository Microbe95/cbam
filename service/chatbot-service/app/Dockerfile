FROM python:3.11-slim

WORKDIR /app
# 이 앱은 절대경로 cbam 의 app 을 말함 
COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]
