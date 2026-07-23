FROM node:alpine

RUN apk add --no-cache tini git \
    && npm install -g git-http-server \
    && adduser -D -g git git

USER git
WORKDIR /home/git

# Bare repository, with anonymous push enabled so we can commit our code to it
RUN git init --bare repository.git \
    && git -C repository.git config http.receivepack true

EXPOSE 3000
ENTRYPOINT ["tini", "--", "git-http-server", "-p", "3000", "/home/git"]
