FROM ubuntu:18.04
LABEL maintainer="cL0und <cL0und@Syclover>"

RUN apt update && apt install -y curl zip vim

ADD jdk1.7.0_21.gz /usr/local/
ENV JAVA_HOME /usr/local/jdk1.7.0_21
ENV CLASSPATH .:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$CLASSPATH
ENV PATH $PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin

RUN useradd tomcat -M
COPY apache-tomcat-7.0.104.zip /usr/local/

COPY ROOT.war /root/

RUN unzip /usr/local/apache-tomcat-7.0.104.zip -d /usr/local/ && \
rm -rf /usr/local/apache-tomcat-7.0.104/webapps/* && \ 
mkdir /usr/local/apache-tomcat-7.0.104/webapps/ROOT && \
unzip /root/ROOT.war -d /usr/local/apache-tomcat-7.0.104/webapps/ROOT/

COPY spring-webflow-client-repo-1.0.0 /root/spring-webflow-client-repo-1.0.0

COPY init.sh /root

RUN keytool -genseckey -alias aes128 -keyalg aes -keypass D5raLiD1inQf3da9 -keysize 128 -keystore /root/spring-webflow-client-repo-1.0.0/etc/cl0und.jceks -storepass nSLn5Z6XchxUBXel -storetype jceks && \
cd /root/spring-webflow-client-repo-1.0.0 && \
zip -r spring-webflow-client-repo-1.0.0.jar ./* && \
mv /root/spring-webflow-client-repo-1.0.0/spring-webflow-client-repo-1.0.0.jar /usr/local/apache-tomcat-7.0.104/webapps/ROOT/WEB-INF/lib && \
chown tomcat:tomcat -R /usr/local/apache-tomcat-7.0.104/ && \
chmod 755 -R /usr/local/apache-tomcat-7.0.104/ && \
chown root:root -R /usr/local/apache-tomcat-7.0.104/webapps/ROOT/

COPY cas-server-support-jdbc-4.1.11.jar /usr/local/apache-tomcat-7.0.104/webapps/ROOT/WEB-INF/lib

COPY mysql-connector-java-5.1.48-bin.jar /usr/local/apache-tomcat-7.0.104/webapps/ROOT/WEB-INF/lib