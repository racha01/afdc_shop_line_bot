FROM python:3.10-slim

WORKDIR /

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py", "--no-debugger",  "--cert=cert.pem", "--key=private.pem"]

