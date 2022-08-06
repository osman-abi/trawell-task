# TRAELL TASK

In this task we use Django, Django REST Framework, JWT Authentication, python stories module,
swagger for api documentation.

## Installation

After clone this respository, follow below sequences

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

After installation all requirements, you can run this app.

## Settings

As you can see, there is a 'VERSION' variable in settings.py file. Database configurations:

```python
if VERSION == 1:
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv('DB_NAME'),
            "USER": os.getenv('DB_USER'),
            "PASSWORD": os.getenv('DB_PASSWORD'),
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
}
```

If you wanna use sqlite3 database you have to initialize '1' to VERSION variable. Otherwise you should change DB_NAME, DB_PASSWORD, DB_USER in your local machine (PGAdmin) for postgreSQL

## Usage

First of all, you need to login for PUT, DELETE, UPDATE methods. Data you sent should be such as:
http://127.0.0.1:8000/api/login/

```bash
{
    "email":"xxxxxx@xxxxxx.com",
    "password":"xxxxxx"
}
```
So, this API responses 'access_token'. You need to use this token in the authorization side, via Bearer.

```bash
{
    'Authorization':'Bearer access_token'
}
```


We have the API url : http://127.0.0.1:8000/api/create/. Your json data have to has 'key' variable. This 'key' variable should contains either 'customer' or 'passport'. If 'key' is customer then Customer model will be created, otherwise Passport model will be created:

### For create Customer json data should be such as below:

```
{
    "key":"customer",
    "name":"test_name_3",
    "surname":"test_surname_3",
    "email":"test-3@email.com",
    "phone":"xxxxxxxx"
}
```

### For create Passport, you need to use form-data in postman:

There are key in Postman form data:
- Key pairs : 'key', 'customer_id', 'scan_file'. 'key' have to equals to 'passport'



