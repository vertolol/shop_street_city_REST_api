

FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /rest_api
WORKDIR /rest_api

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./rest_api /rest_api
COPY ./config/gunicorn /config/gunicorn

CMD ["gunicorn", "-c", "../config/gunicorn/conf.py", "--chdir", "rest_api", "rest_api.wsgi:application"]