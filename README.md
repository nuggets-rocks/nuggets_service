# Nuggets of Wisdom

This is the back-end service for the Nuggets app. It is meant to be a REST API serving data to various clients

## Setup

Make sure you have Python 3.7 and pip installed
* Mine was installed in `/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7` (installed with brew)
* pip3.7 should be installed with this^ 

Make sure you have django and mysqlclient installed 
* `pip3.7 install django`
* `pip3.7 install mysqlclient`

Make sure you have mysql >5.6 installed (I used brew)
* `brew install mysql`

Set up the database with the following commands:
* `mysql -u root`
* `CREATE DATABASE nuggets CHARACTER SET utf8;`
* `CREATE USER 'nuggets'@'localhost' IDENTIFIED BY 'karthikrocks';`
* `GRANT ALL PRIVILEGES ON nuggets.* TO 'nuggets'@'localhost';`

Run django migrations and server:
* `python3.7 manage.py migrate`
* `python3.7 manage.py runserver`
* `pip3 install djangorestframework`

Visit http://localhost:8000 and see something

## Troubleshooting
* Error: `django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module. Did you install mysqlclient?`
* Solution:
pip3.7 install pymysql
Then, edit the __init__.py file in your project origin dir(the same as settings.py)
add:
```
import pymysql
pymysql.install_as_MySQLdb()
```
source https://stackoverflow.com/questions/46902357/error-loading-mysqldb-module-did-you-install-mysqlclient-or-mysql-python

* Error: `raise RuntimeError("cryptography is required for sha256_password or caching_sha2_password")
RuntimeError: cryptography is required for sha256_password or caching_sha2_password`
* Solution: pip3.7 install cryptography

* Error: "Table 'nuggets.nuggets_api_nuggetuser' doesn't exist"
* Solution: python3.7 manage.py makemigrations [We regenerate the dB from the model]

## Sample requests
```
curl -XGET https://nuggets-service.herokuapp.com/api/v0/user/3/review/ -H
'Authorization: Token e507c000d665511ac464c9251f7ef277d9b72296' | jq .
```

## Update schema after model change

Our deployed heroku app is running postgressql and so seems like running python migration won't regen the database. To
update the scheme, manually modify the schema:

```
heroku run python manage.py dbshell --app nuggets-service

ALTER TABLE nuggets_api_nugget ADD COLUMN url text;
```