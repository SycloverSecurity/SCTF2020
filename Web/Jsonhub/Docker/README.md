由于挂在了log目录，现在当前目录创建log文件，  赋予777
然后
编辑app/web1/app/views.py 49行

替换为将自己的主机的ip（非127.0.0.1即可，内外网ip都行）

docker-compose up -d
访问 http://ip:80/
即可
