FROM python:2.7
RUN mkdir -p /opt/www/featurette
ADD ./featurette/requirements.txt /opt/www/featurette/requirements.txt
RUN pip install -r /opt/www/featurette/requirements.txt
VOLUME /opt/www/featurette
WORKDIR /opt/www/featurette
EXPOSE 5000
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /tmp && chmod +x /tmp/wait-for-it.sh
# CMD /tmp/wait-for-it.sh db:3306 -- python db_create.py && python run.py
CMD /tmp/wait-for-it.sh db:3306 -- python run.py
