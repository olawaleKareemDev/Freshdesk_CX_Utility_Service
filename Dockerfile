FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR  /app
COPY  requirements.txt /app/requirements.txt
RUN   python -m pip install --upgrade pip
RUN   pip install -r requirements.txt
COPY . /app
CMD gunicorn freshsales_automations.wsgi:application