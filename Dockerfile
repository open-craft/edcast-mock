FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt


COPY . /app
ENTRYPOINT ["flask"]
CMD ["--app", "app", "run", "--debug"]

