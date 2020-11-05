# rtmp-relay-obs
Relais RTMP vers nginx avec deux trois trucs sympas


main.py --source=rtmp://faeziuhbazoeiufhabzeoifuahn/ke
-> aller en db voir si le flux existe
-> si oui: planter, renvoyer le lien existant, return
-> si non:
    -> créer la session nginx sur passerelle
    -> créer l'entrée en db avec pid(primaire)/lien interne rez/lien externe/matire, prof, infos du cul
    -> return lien interne

www.obs.rez pour voir tous les flux

Si besoin :
main.py --kill=truc
-> tuer "truc" si existant (session nginx)

C'est une rediff ?


  Template fichier config partie RTMP:
  rtmp {
      server {
          listen 1935;
          chunk_size 4096;

      application pullfrompublisher {
          live on;
          record off;
          pull rtmp://10.2.4.5:2935/ocpush/cnoc live=1;
          }

      application pushtotwitch {
          live on;
          record off;
          push rtmp://live.twitch.tv/live/streamkey;
          }
      }
  }


FICHIER DE BASE:
  #user  nobody;
  worker_processes  1;

  #error_log  logs/error.log;
  #error_log  logs/error.log  notice;
  #error_log  logs/error.log  info;

  #pid        logs/nginx.pid;


  events {
      worker_connections  1024;
  }


  http {
          include       mime.types;
          default_type  application/octet-stream;

          #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
      #                  '$status $body_bytes_sent "$http_referer" '
          #                  '"$http_user_agent" "$http_x_forwarded_for"';

          #access_log  logs/access.log  main;

          sendfile        on;
          #tcp_nopush     on;

          #keepalive_timeout  0;
          keepalive_timeout  65;

          #gzip  on;

          server {
                  listen       80;
                  server_name  localhost;

                  #charset koi8-r;

                  #access_log  logs/host.access.log  main;

                  location / {
                          root   html;
                          index  index.html index.htm;
                  }

                  #error_page  404              /404.html;

                  # redirect server error pages to the static page /50x.html
                  #
                  error_page   500 502 503 504  /50x.html;
                  location = /50x.html {
                          root   html;
                  }

                  # proxy the PHP scripts to Apache listening on 127.0.0.1:80
                  #
                  #location ~ \.php$ {
                  #    proxy_pass   http://127.0.0.1;
                  #}

                  # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
                  #
                  #location ~ \.php$ {
                  #    root           html;
                  #    fastcgi_pass   127.0.0.1:9000;
                  #    fastcgi_index  index.php;
                  #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
                  #    include        fastcgi_params;
                  #}

                  # deny access to .htaccess files, if Apache's document root
                  # concurs with nginx's one
                  #
                  #location ~ /\.ht {
                  #    deny  all;
                  #}
          }
    }
