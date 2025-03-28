release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn social_media_api.wsgi --log-file -