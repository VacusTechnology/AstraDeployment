#/bin/sh
cd /home/ec2-user/backend
/usr/local/bin/uwsgi --socket :8000 --module backend.wsgi -p 20
