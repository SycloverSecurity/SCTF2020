FROM python:3.6.9


COPY sources.list /etc/apt/sources.list

RUN apt update
RUN apt install python3 python3-pip vim net-tools libmariadb-dev curl -y
RUN apt install mariadb-server-10.3 -y

COPY app /app
COPY start.sh /start.sh
COPY default /etc/nginx/sites-available/default
COPY flag /flag
RUN pip3 install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ && pip3 install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN chmod 755 -R /app && useradd ctf && chmod 777 /start.sh && chmod 744 /flag


CMD ["bash","/start.sh"]
