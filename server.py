#!/usr/bin/env python

# WS server that run command from server
# send command like this from server:
# ifconfig
# df
# "for i in {1..3}; do sleep 1 && echo \"current time: `date`\"; done"

import asyncio
import datetime
import random
import websockets
import subprocess

async def run_cmd(websocket, path):
    async for message in websocket:
        print(f">  {message}")
        greeting = f"> {message}"
        await websocket.send(greeting)

        if message:
            print ('Recieved from ' + str(websocket.remote_address) + ': ' + message)

            # For Linux, use '/bin/sh ', for windows: cmd.exe /c
            # "universal newline support" :
            # This will cause to interpret \n, \r\n and \r  equally, each as a newline String (not bytes).
            proc = subprocess.Popen('/bin/sh -c ' + message, shell=True, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                bufsize=1, universal_newlines=True)

            for line in proc.stdout:
                line = line.rstrip()
                print(f"line = {line}")
                await websocket.send(line) #line.decode('utf-8') if universal_newlines not specified
            # if the process has completed:
            print("command done!")
            await websocket.send("done!")
        else:
            await websocket.send('Non unicode data received! Send text please :)')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(run_cmd, 'localhost', 5678))

asyncio.get_event_loop().run_forever()