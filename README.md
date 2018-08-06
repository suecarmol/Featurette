# Featurette

[![Build Status](https://travis-ci.org/suecarmol/Featurette.svg?branch=master)](https://travis-ci.org/suecarmol/Featurette)

Featurette is an app that helps you create and manage feature requests for different clients and product areas.

## Instructions

```shell
git clone https://github.com/suecarmol/Featurette.git
```

```shell
cd Featurette
```

```shell
docker-compose build
```

```shell
docker-compose up
```

```shell
docker exec -it featurette_www_1 python db_create.py
```

## Testing

```shell
docker exec -it featurette_www_1 python -m unittest discover -v tests
```

## Tools Used

* Semantic UI - UI Framework
* Flask Framework - Backend API
    * Flask-Login
    * Flask-Restful
    * Flask-Bcrypt
    * Flask-SQLAlchemy
* JQuery - Frontend
* Knockout JS - Frontend
* Docker - Container
* MySQL - Database used
