FROM python:3.13.7-alpine3.22

WORKDIR /app

COPY requirements.txt src/ static/ content/ install.sh sidewinder.sh /app

#NOTE: Use docker volume for persistent storage of output site

RUN ./install.sh

ENTRYPOINT ["sidewinder.sh"]
