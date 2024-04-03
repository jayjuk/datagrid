import tornado.ioloop
import tornado.web
import tornado.websocket
import datetime
import asyncio


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        print("WebSocket opened")
        self.clients.add(self)

    def on_message(self, message):
        print(f"Received message: {message}")

    def on_close(self):
        print("WebSocket closed")
        self.clients.remove(self)

    def check_origin(self, origin):
        return True  # Allow connections from any origin


async def send_updates():
    while True:
        for client in SimpleWebSocket.clients:
            message = f"Server time is {datetime.datetime.utcnow().isoformat()}"
            client.write_message(message)
        print("ping")
        await asyncio.sleep(5)  # Wait for 5 seconds before sending the next message


def make_app():
    return tornado.web.Application(
        [
            (r"/websocket", SimpleWebSocket),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    print("Listening on http://localhost:8080")
    loop = tornado.ioloop.IOLoop.current()
    loop.spawn_callback(send_updates)
    loop.start()
