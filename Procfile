release: python manage.py migrate
release: django-admin makemessages -a
web: gunicorn basta_app.wsgi --log-file -
