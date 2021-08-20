FROM centos:7
WORKDIR /srv

RUN yum install -y socat && yum clean all

ADD chal /srv/challenge
ADD database.txt /srv/
RUN chmod +x /srv/challenge

EXPOSE 5000

RUN useradd -M -s /usr/bin/nologin ctf
USER ctf
ENTRYPOINT ["socat", "-s", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge,stderr"]
