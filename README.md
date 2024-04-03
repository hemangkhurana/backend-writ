This repo contains backend for DSS version writ management only. Django is used as backend framework with postgresql and mongodb has databases.

To use this repo in local machine, one can either
  1. first log into their terminal with their github account and use `git clone [repo name]` command to copy this repo.
       `git clone https://github.com/hemangkhurana/backend-writ.git`
  2. download zip from repo and unzip it in their required folder.

Repo contains two django applicaiton, named Common and Writ, where common stores backend logic for website use only and writ stores all the writ related logic.

## Common: 
- One can access the common app in the folder `writManagement/common`. It contains views for login and signup which uses Postgresql database that has been hosted on Google Cloud. 
- Login procedure uses JWT tokens for secure logins and one can add/remove fields according to their needs.
- Credntials for database and important information for all apps are stored in `writManagement/writManagement/settings.py`.

## Writ:
- Writ data is stored in MongoDB database which is hosted on mondodb website. Credentials are saved in `writManagement/writ/mongodb_connection.py`
- Multiple views are present in `writManagement/writ/views.py` responsible for all logic.
- Step by step explanation for each component in the website :
    - 
