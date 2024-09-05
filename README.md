# GitGang-HMS-Web-Mobile
This is a group repository for the GitGang group.

# Main Branch Rules
- please dont change
- only allowed admins can change for version control

# Installation
suppose your were able to clone the project
now you need to run it safely 

1. You need an envrionment, so go into the main Gitgang-hms-web-mobile folder
```Bash
python -m venv hms-venv
```

2. Now activate the environment, go into your hms-venv/Scripts in CMD preferably
```Bash
activate
```
if it doesnt work mayb you are in Powershell
```Bash
Activate.bat
```
3. Now we need to configure the project to work optimally, go into the hms_gitgang folder
4. Now you can start downloading the requirements
```Bash
pip install -r requirements.txt
```
5. after everything has been installed nothing should be missing
6. you need to configure the database, please have docker for this step
```Bash
docker-compose up -d
```
7. if you dont have docker you need to change a couple settings in the settings.py file
```python
# this is if you dont have docker - for development only
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
     }
} 

# for production - please use this one also if you have docker installed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),  # This should match the service name in docker-compose.yml
        'PORT': os.getenv("DB_PORT"),
    }
}
```
8. You just finished configuring the database, now you need to do some migrations
9. This will only work in the root hms_gitgang folder where the manage.py file is in
10. if you experience any error, please check you are in the right folder/path
```Bash
python manage.py makemigrations
```
11. Your makemigrations command has ran successfully, now you can migrate the database
```Bash
python manage.py migrate
```
12. if you are in docker your database server is running good but make sure if you are in production this is turned off
this must be False if you are in production but lets say you are in development then this should be True
```python
# If you want to allow all origins (not recommended for production):
CORS_ALLOW_ALL_ORIGINS = False
```
but lets say you want to specify the domain/hosts that can access the API this is where you allow them
```python
# CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5432",
]
```

