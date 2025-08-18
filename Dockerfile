FROM python:3.13.7-alpine3.22

WORKDIR /app

COPY requirements.txt src/ static/ content/ install.sh sidewinder.sh /app

RUN ./install.sh

ENTRYPOINT ["sidewinder.sh"]
