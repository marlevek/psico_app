# PSICO_APP/Procfile (Sem extensão)

release: python manage.py migrate --noinput
web: gunicorn app_core.wsgi:application