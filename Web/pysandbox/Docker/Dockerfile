FROM python:3.8.3

COPY app /app/

WORKDIR /app/
RUN useradd ctf && chmod 755 -R /app

RUN pip install uwsgi flask==1.1.2 -i https://pypi.tuna.tsinghua.edu.cn/simple/

USER ctf

CMD ["python","app.py"]




