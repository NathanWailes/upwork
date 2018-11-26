FROM python:3

ADD __init__.py /app/
ADD main.py /app/
ADD pull_pubsub_messages.py /app/
ADD query_bigdata_table_size.py /app/

ADD requirements.txt /app/

RUN pip install -r /app/requirements.txt

# https://stackoverflow.com/a/33379487/4115031
ENV GOOGLE_APPLICATION_CREDENTIALS="./google_application_credentials.json"

CMD [ "python", "./app/main.py" ]
