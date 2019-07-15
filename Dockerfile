FROM python:3.6-alpine3.9

COPY . .

RUN apk update && apk add curl gcc libxml2 libxslt 	libxslt-dev libxml2-dev  musl-dev freetype-dev libjpeg-turbo-dev libpng-dev && pip install nltk && curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3

#HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1
RUN pip install pipenv --upgrade && pipenv install 

CMD ["pipenv", "run", "celery", "-A", "tasks", "worker", "-B", "--loglevel=info"]
