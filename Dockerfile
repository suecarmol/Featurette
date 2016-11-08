FROM python:2.7
COPY . /opt/www
WORKDIR /opt/www/featurette
RUN pip install -r requirements.txt
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /tmp && chmod +x /tmp/wait-for-it.sh
CMD /tmp/wait-for-it.sh db:3306 -- python db_create.py && python run.py
