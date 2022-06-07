FROM python:3.8
WORKDIR /app
COPY . .
RUN pip3 install pipenv
RUN pipenv shell && pipenv install
ENTRYPOINT [ "python3", "run.py" ]