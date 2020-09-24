FROM ubuntu:18.04

RUN apt-get update

# nginx content dirs
RUN mkdir -p /data/www
RUN mkdir -p /data/images
WORKDIR /data/
ADD ./index.html /data/www/
ADD ./pic /data/www/
ADD ./hello.html /data/www/

# nginx installation
RUN apt-get install -y curl
RUN apt-get install -y gnupg2
RUN apt-get install -y ca-certificates
RUN apt-get install -y lsb-release 
RUN echo "deb http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
 | tee /etc/apt/sources.list.d/nginx.list
RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add - >> install_log 2>>inst_err_log
RUN apt-key fingerprint ABF5BD827BD9BF62
RUN apt-get install -y nginx

# nginx config
#RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080
EXPOSE 80

CMD [ "/usr/sbin/nginx" ]
#CMD [ "cat", "/etc/nginx/nginx.conf" ]
