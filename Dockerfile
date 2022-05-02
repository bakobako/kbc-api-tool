FROM python:3.8-alpine
WORKDIR /var/www

COPY ./app.py /var/www/app.py
COPY ./templates /var/www/templates
COPY ./src /var/www/src
COPY ./static /var/www/static
COPY ./static /var/www/images
COPY ./requirements.txt /var/www/requirements.txt
COPY ./gunicorn_config.py /var/www/gunicorn_config.py

RUN pip install -r /var/www/requirements.txt

CMD gunicorn --config gunicorn_config.py --worker-tmp-dir /dev/shm app:app
