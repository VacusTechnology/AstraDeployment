#/bin/sh
cd /home/ubuntu/backend
/usr/local/bin/uwsgi --socket :8000 --module backend.wsgi -p 20
