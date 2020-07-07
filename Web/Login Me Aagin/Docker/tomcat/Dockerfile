FROM ubuntu:16.04
LABEL maintainer="cL0und@Syclover , leixiao@Syclover"
ADD apache-tomcat-8.5.0.tar.gz /
ADD jre-8u251-linux-x64.tar.gz /
COPY ROOT.war /
COPY flag.txt /
ENV JRE_HOME /jre1.8.0_251
RUN rm -rf /apache-tomcat-8.5.0/webapps/* && \
    mv /ROOT.war /apache-tomcat-8.5.0/webapps/ && \
    useradd -m ctfer && \
    chown -R ctfer /apache-tomcat-8.5.0
USER ctfer