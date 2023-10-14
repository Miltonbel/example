FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3002

LABEL author="mj.beltran37@uniandes.edu.co"

CMD ["gunicorn", "-b", "0.0.0.0:3002", "app:app"]