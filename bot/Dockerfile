FROM python:3.10.12-alpine

WORKDIR /usr/app
ENV PYTHONPATH=/usr/app/src

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "src/bot.py"]