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
Install Nomachine to run for both devices to set up remote connect 

fix the next file 
/usr/NX/etc/server.cfg

uncommit the next row:
CreateDisplay 1

and set this key:
DisplayOwner USERNAME
