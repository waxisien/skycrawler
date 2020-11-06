FROM python:3.7-slim

EXPOSE 80

RUN pip install --no-cache gunicorn==20.0.4

WORKDIR /opt/src/skycrawler/

# copy files on the workdir so we can install it
COPY . ./
#ARG TAG
#RUN echo $TAG > version
RUN pip install --no-cache .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "skycrawler.app:create_app()"]
