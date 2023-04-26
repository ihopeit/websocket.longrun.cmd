# Install dependencies
python3.8 -m pip install fastapi uvicorn

# Start the server
uvicorn main:app --reload

# How to send message to specified client

First identify each client with a client_id, and save it.
Then in an async task, can send message to the client by client_id.

## Send message to one client by client_id through HTTP post
curl -H 'Content-Type: application/json' -s -X POST http://127.0.0.1:8000/send/1682497472881 -d '{"text":"hello world from background job"}'
