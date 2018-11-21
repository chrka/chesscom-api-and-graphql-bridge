FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV PYTHONPATH /app

ENV EXPOSE_GRAPHQL_BRIDGE YES

CMD ["python", "-m", "cgqlbridge"]