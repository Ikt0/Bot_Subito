FROM python:3.12.3-alpine3.18
COPY . /app
RUN pip install requests
RUN pip install playsound
CMD python /app/botSubito.py