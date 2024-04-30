1) install poetry

2) run
poetry install

3) install clickhouse

4) run
 ./clickhouse server

5) run 
./clickhouse client

6) create table with columns:
datas: json
timestamp:timestam(not sure column type)

7) run fastapi server:
uvicorn main:app --reload



Appendix:

*Install Nomachine to run for both devices to set up remote connect 

fix the next file 
/usr/NX/etc/server.cfg

uncommit the next row:
CreateDisplay 1

and set this key:
DisplayOwner USERNAME


* Install NGINX
intall nginx
create a new file
sudo nano /etc/nginx/sites-available/devices

set up the next row int he file
server {
    listen 80;
    server_name -.-.-.-; # host of your device

    location / {
	proxy_pass http://127.0.0.1:8000; # указанный порт должен соответствовать порту сервера Uvicorn
	proxy_set_header Host $host; # передаем заголовок Host, содержащий целевой IP и порта сервера.
	proxy_set_header X-Real-IP $remote_addr; # передаем заголовок с IP-адресом пользователя
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # передаем всю последовательность адресов, через которые прошел запрос
    }
}

create the link:

sudo ln -s /etc/nginx/sites-available/devices /etc/nginx/sites-enabled


check:
sudo nginx -t

restart:
sudo systemctl restart nginx


allow nginx to ufw:
sudo ufw allow 'Nginx Full'
