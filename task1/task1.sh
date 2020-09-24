# /bin/bash -e

docker build -t nginx:ubuntu .
docker run --rm -p 8080:8080 nginx:ubuntu
