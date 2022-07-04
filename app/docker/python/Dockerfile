# pull official base image
FROM python:3.8-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/

RUN pip install flask
# copy project
COPY . /usr/src/app/

COPY requirements.txt /docker/python/requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "run.py"]