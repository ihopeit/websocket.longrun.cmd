# Install dependencies
python3.8 -m pip install fastapi uvicorn

# Start the server
uvicorn main:app --reload

# How to send message to specified client

First identify each client with a client_id, and save it.
Then in an async task, can send message to the client by client_id.

## Send message to one client by client_id through HTTP post
curl -H 'Content-Type: application/json' -s -X POST http://127.0.0.1:8000/send/1682497472881 -d '{"text":"hello world from background job"}'

# Websocket examples

* FastAPI WebSocket: https://fastapi.tiangolo.com/advanced/websockets/
* Secure WebSocket server: https://websockets.readthedocs.io/en/stable/howto/quickstart.html#secure-server-example
* An example to track user data in websocket: https://github.com/manemotha/Rooms/blob/master/main.py
* FastAPI QuickStart: https://fastapi.tiangolo.com/#requirements

# FastAPI WebSocket over SSL/TLS:
* https://stackoverflow.com/questions/68330775/how-to-make-websocket-secure-wss-connections-in-fastapi
* https://www.uvicorn.org/deployment/#running-with-https

```
$ uvicorn example:app --port 5000 --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
```

Running gunicorn worker
It's also possible to use certificates with uvicorn's worker for gunicorn.
```
$ gunicorn --keyfile=./key.pem --certfile=./cert.pem -k uvicorn.workers.UvicornWorker
```

# Load balance WebSocket
* https://github.com/nicokaiser/nginx-websocket-proxy/tree/master
* https://www.nginx.com/blog/websocket-nginx/
* https://stackoverflow.com/questions/73335010/how-to-set-fastapi-websocket-properly-with-nginx
* Performance: https://www.nginx.com/blog/nginx-websockets-performance/
  
The WebSocket protocol is different from the HTTP protocol, but the WebSocket handshake is compatible with HTTP, using the HTTP Upgrade facility to upgrade the connection from HTTP to WebSocket. This allows WebSocket applications to more easily fit into existing infrastructures. 

For example, WebSocket applications can use the standard HTTP ports 80 and 443, thus allowing the use of existing firewall rules.

# WebSocket on Django
* https://websockets.readthedocs.io/en/stable/howto/django.html

# Conf for Websocket on nginx

https://github.com/nicokaiser/nginx-websocket-proxy/tree/master

Requirements
* nginx 1.4.x or higher
* WebSocket and HTTP server running on ws|http://localhost:8080

This is a typical scenario given by Engine.IO, Socket.IO, Primus, etc. which provide a WebSocket server with HTTP fallback. 

Forwards WSS and HTTPS requests to ws|http://localhost:8080
WSS and HTTPS shares the same port 443.

```
# WebSocketSecure SSL Endpoint
#
# The proxy is also an SSL endpoint for WSS and HTTPS connections.
# So the clients can use wss:// connections 
# (e.g. from pages served via HTTPS) which work better with broken 
# proxy servers, etc.

server {
    listen 443;

    # host name to respond to
    server_name ws.example.com;

    # your SSL configuration
    ssl on;
    ssl_certificate /etc/ssl/localcerts/ws.example.com.bundle.crt;
    ssl_certificate_key /etc/ssl/localcerts/ws.example.com.key;

    location / {
        # switch off logging
        access_log off;

        # redirect all HTTP traffic to localhost:8080
        proxy_pass http://localhost:8080;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # WebSocket support (nginx 1.4)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Proxy pass all incoming request to 8080.

```
# WebSocket Proxy with Path Rewriting
#
# Like the other examples, but HTTPS and WSS endpoints are not "/" but 
# "/services/myservice/". So something like 
# "wss://api.example.com/services/myservice" can be done.

server {

    # see simple-wss.conf or simple-ws.conf

    location /services/myservice {
        # switch off logging
        access_log off;

        # redirect all HTTP traffic to localhost:8080
        proxy_pass http://localhost:8080;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # WebSocket support (nginx 1.4)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Path rewriting
        rewrite /services/myservice/(.*) /$1 break;
        proxy_redirect off;
    }
}
```


Load Balance

```
# WebSocket Proxy with Load Balancing
#
# Like the other examples, but there are three WS backends (ws1, ws2, ws3).
# Each client must always be forwarded to the same backend (e.g. when using 
# HTTPS requests).

upstream myservice {
    # Clients with the same IP are redirected to the same backend
    ip_hash;

    # Available backend servers
    server ws1.example.com:8080;
    server ws2.example.com:8080;
    server ws3.example.com:8080;
}


server {

    # see simple-wss.conf or simple-ws.conf

    location /services/myservice {
        # switch off logging
        access_log off;

        # redirect all HTTP traffic to localhost:8080
        proxy_pass http://myservice;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # WebSocket support (nginx 1.4)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Path rewriting
        rewrite /services/myservice/(.*) /$1 break;
        proxy_redirect off;
    }
}

```