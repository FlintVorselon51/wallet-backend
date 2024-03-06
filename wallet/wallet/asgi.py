import os

from django.core.asgi import get_asgi_application

path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

if os.path.isfile(os.path.join(path, 'local_settings.py')):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")
else:
    raise FileNotFoundError(
        "Couldn't find settings file. Create local_settings.py in"
        "Django root directory and set SECRET_KEY and DATABASES there."
    )

application = get_asgi_application()
