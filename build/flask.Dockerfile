FROM python:3.12.7

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app/main.py

CMD ["flask", "run", "--host=0.0.0.0"]