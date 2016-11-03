FROM python:2.7
COPY . /opt/www
WORKDIR /opt/www/featurette
RUN pip install -r requirements.txt
CMD python db_create.py && python run.py
