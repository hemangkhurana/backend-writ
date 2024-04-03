## Getting Started
This repository contains backend for DSS version writ management only. Django is used as backend framework with Postgresql and MongoDB as databases.

To clone this repo in local machine, one can either
  1. First log into their terminal with their github account and use `git clone [repo name]` command to copy this repo. <br>
     `git clone https://github.com/hemangkhurana/backend-writ.git`
  2. Download zip from repo and unzip it in their required folder.

Repo contains two django applicaiton, named Common and Writ, where common stores backend logic for website use only and writ stores all the writ related logic.<br>
Connection data for postgesql is present in `writManagement/writManagement/settings.py` and `writManagement/writ/mongodb_connection.py` for mongoDB.

<br>

### `python manage.py runserver`
Use above command in terminal to run backend in local machine in development mode. Make sure that relevant frontend is also running. Errors, if present, will be seen on temrinal window.
Refer The development server part of  [Writing your first Django app](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)

<br> 

## Deployment in Production mode
Current deploy is done through Gunicorn and Nginx in linux based enviornment. Current version is hosted on Virtual Machine on Google Cloud.

Refer to [Host Django Application using gunicorn & nginx in Production](https://www.codewithharry.com/blogpost/django-deploy-nginx-gunicorn/) for specific instructions.

Also refer [How to deploy Django](https://docs.djangoproject.com/en/5.0/howto/deployment/) for other methods of deployment.

<br>

## Learn More
Follow tutorials to learn more about [Django](https://docs.djangoproject.com/en/5.0/intro/install/)

### Virtual Enviornment
Setup [virtual environment for Django](https://www.javatpoint.com/django-virtual-environment-setup)

### Getting SSL certificate
Refer to [SSL/TLS Certificates with NGINX](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/) for SSL certificate and HTTPS on the website
