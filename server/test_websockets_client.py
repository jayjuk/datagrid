import asyncio
import websockets

async def listen(uri):
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")

if __name__ == "__main__":
    # Replace "ws://localhost:8080/websocket" with the WebSocket server URI you want to connect to
    uri = "ws://localhost:8080/websocket"

    asyncio.run(listen(uri))
