# websocket.longrun.cmd: A web socket server for long running command

A demo for python web socket.
You can send a shell command from the web page.
The websocket server will get the command, fire the command, and send back command output to the web page line by line in real time.

For long running command, the output will be shown on the web page continuously.

## Start the server

pip install websockets
python3 server

Then you can open the client.html in your browser and run command.
You can enter command like this:

* df
* ifconfig
* "for i in {1..3}; do sleep 1 && echo \"current time: `date`\"; done"
* "tail -f /data/logs/abc.log"

The last 2 commands is test for long running command.
For the tail command, if new content saved to the abc.log, the new logs will show up on the web page in real time.