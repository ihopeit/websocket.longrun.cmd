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

The WebSocket protocol is different from the HTTP protocol, but the WebSocket handshake is compatible with HTTP, using the HTTP Upgrade facility to upgrade the connection from HTTP to WebSocket. This allows WebSocket applications to more easily fit into existing infrastructures. 

For example, WebSocket applications can use the standard HTTP ports 80 and 443, thus allowing the use of existing firewall rules.

# WebSocket on Django
* https://websockets.readthedocs.io/en/stable/howto/django.html
