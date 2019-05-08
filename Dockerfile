FROM python:3.6-slim
COPY . /root/nslab
WORKDIR /root/nslab/
RUN pip install -r requirements.txt
WORKDIR  /root/nslab/src/
Expose 8000
CMD python manage.py runserver 0.0.0.0:$PORT
