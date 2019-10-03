

FROM python:3.7

RUN mkdir /rest_api
WORKDIR /rest_api

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./rest_api /rest_api

EXPOSE 5000

CMD ["gunicorn", "--bind", ":5000", "--chdir", "rest_api", "rest_api.wsgi:application"]