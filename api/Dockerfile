FROM python:3.10.12-alpine

WORKDIR /usr/app
ENV PYTHONPATH=/usr/app/src

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]