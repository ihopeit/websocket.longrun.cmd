from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.collection_map: map[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.collection_map[websocket.client_id] = websocket

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.collection_map.pop(websocket.client_id)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
    async def send_message_by_client(self, message: str, client_id: int):
        websocket: WebSocket = self.collection_map.get(client_id)
        print("sending message to client:%s" % client_id )
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)

## a post method to receive message and a client id to send the message to the client
@app.post("/send/{client_id}")
async def send_message(client_id: int, message: dict):
    print("send message to client_id:%s message:%s" % (client_id, message))
    await manager.send_message_by_client(message.get("text"), client_id)
    return {"message": message, "client_id": client_id}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    websocket.client_id = client_id # can append new properties to WebSocket object
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
