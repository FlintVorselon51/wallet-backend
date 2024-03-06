# Wallet Backend

## Project setup

Create and activate virtual environment for the project:

```commandline
python -m venv venv
source venv/bin/activate
```

Install all necessary packages to your virtual environment:

```commandline
pip install -r requirements.txt
```

Create local_settings.py in Django project root directory:

```
wallet-backend
│    README.md               <- You are probably here
└─── wallet                  <- django project root directory
│   │   local_settings.py    <- Create this file
│   │   manage.py
│   │   ...
```

You need to fill this file with some private settings like `SECRET_KEY` and `DATABASES`.
Also, you can add or any django setting you need.
In this file you need to import all settings from `development.py` or `production.py`.
These files contain base settings for the project settings.

Here is an example of `local_settings.py`:

```python
from wallet.settings.development import *

SECRET_KEY = '1234'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Synchronize your database state with the current set of models and migrations:

```commandline
python manage.py migrate
```

If you want, you can fill your database with prepared data:

```commandline
python manage.py fill_db
```

Now, you can run the server:

```commandline
python manage.py runserver
```

## Links

[Frontend repository](https://github.com/hitasher/wallet-frontend)
