## start mysql
service mysql start

## create database
mysql -uroot -e "create database django"

## change password
mysql -uroot -e "use mysql;UPDATE user SET plugin='mysql_native_password', authentication_string=PASSWORD('root') WHERE User='root';FLUSH PRIVILEGES;"

## init database
python3 /app/web1/manage.py makemigrations
python3 /app/web1/manage.py migrate app
python3 /app/web1/manage.py migrate

## create token
mysql -uroot -proot -e "insert into django.app_token values(1,'`head -c 32 /dev/random | md5sum | head -c 32`');"

## start service
uwsgi /app/web1/uwsgi.ini
uwsgi /app/web2/uwsgi.ini