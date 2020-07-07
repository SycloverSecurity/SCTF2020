FROM ubuntu:16.04
LABEL maintainer="cL0und@Syclover , leixiao@Syclover"
ADD jre-8u251-linux-x64.tar.gz /
COPY sctf2020_jar-0.0.1-SNAPSHOT.jar /
COPY hint.txt /
RUN apt update && \
    apt install -y net-tools && \
    apt install -y iputils-ping && \
    apt install -y netcat && \
    apt install -y curl && \
    useradd -m ctfer
USER ctfer

