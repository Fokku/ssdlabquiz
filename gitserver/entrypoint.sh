#!/bin/sh
# Seed the bare repository from the project's own git history (mounted at
# /seed by docker-compose), so a fresh machine serves the full commit
# history immediately after "docker-compose up".
if [ -e /seed/HEAD ]; then
    git config --global safe.directory '*'
    git -C /home/git/repository.git fetch /seed '+refs/heads/*:refs/heads/*' \
        || echo "WARN: seeding from /seed failed; serving repository as-is"
    git -C /home/git/repository.git symbolic-ref HEAD refs/heads/main || true
fi
exec git-http-server -p 3000 /home/git
