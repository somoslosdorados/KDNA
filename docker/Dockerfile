FROM debian:12.4

ARG SSH_PUB_KEY

USER root

RUN useradd -ms /bin/bash test
RUN echo "test:test" | chpasswd
WORKDIR /home/test

RUN apt update && apt install -y \
    openssh-server && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /run/ssh && \
    mkdir -p /var/run/sshd


USER test



RUN mkdir -p /home/test/.ssh && \
    echo "$SSH_PUB_KEY" > /home/test/.ssh/authorized_keys && \
    chmod 700 /home/test/.ssh && \
    chmod 600 /home/test/.ssh/authorized_keys

USER root


EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
