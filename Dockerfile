FROM python:3.12.3-alpine3.18
COPY . /app
RUN pip install requests
RUN pip install playsound==1.2.2
RUN pip install beautifulsoup4
RUN pip install db-sqlite3
CMD python /app/bot_subito.py