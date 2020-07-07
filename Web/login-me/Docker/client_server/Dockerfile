FROM ubuntu:18.04
LABEL maintainer="cL0und <cL0und@Syclover>"

RUN apt update && apt install -y curl zip vim openjdk-8-jdk
COPY apache-tomcat-7.0.104.zip /usr/local/
RUN unzip /usr/local/apache-tomcat-7.0.104.zip -d /usr/local/ && rm -rf /usr/local/apache-tomcat-7.0.104/webapps/*
COPY ROOT.war /usr/local/apache-tomcat-7.0.104/webapps/

RUN useradd tomcat -M && \
chown tomcat:tomcat -R /usr/local/apache-tomcat-7.0.104/ && \
chmod 755 -R /usr/local/apache-tomcat-7.0.104/

COPY init.sh /root