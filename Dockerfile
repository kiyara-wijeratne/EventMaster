# adapted from
# https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/
# https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/
# https://thenewstack.io/how-to-use-the-docker-exec-command/

FROM python:3.12
WORKDIR /app

# install application dependencies 
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy in source code
COPY . .
EXPOSE 8080

CMD python seed.py && flask run --host=0.0.0.0 --port=8080