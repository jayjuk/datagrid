import os
import os.path
import logging
import tornado.websocket
import tornado.web
import tornado.ioloop
import threading
import concurrent.futures
import pandas as pd
import numpy as np
from datetime import date, datetime


from perspective import Table, PerspectiveManager, PerspectiveTornadoHandler


here = os.path.abspath(os.path.dirname(__file__))

IS_MULTI_THREADED = True

import time

import random
import traceback


def generate_random_update():
    """Generates a random update for the table."""
    # Generate an update for a single row. Adjust according to your data structure.
    update = {
        "int": [
            random.randint(0, 99)
        ],  # Assuming 'int' is a unique identifier for rows
        "float": [random.random() * 100],
        "bool": [random.choice([True, False])],
        "date": [date.today()],
        "datetime": [datetime.now()],
        "string": [str(random.randint(100, 999))],
    }
    print(update)
    return update


def perspective_thread(manager, table):
    """Perspective application thread that periodically updates the table."""
    psp_loop = tornado.ioloop.IOLoop()
    manager.host_table("data_source_one", table)

    # Function to periodically update the table
    def updater():
        update = generate_random_update()
        table.update(update)

    callback = tornado.ioloop.PeriodicCallback(callback=updater, callback_time=1000)

    psp_loop = tornado.ioloop.IOLoop()
    if IS_MULTI_THREADED:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            manager.set_loop_callback(psp_loop.run_in_executor, executor)
            callback.start()
            psp_loop.start()
    else:
        manager.set_loop_callback(psp_loop.add_callback)
        callback.start()
        psp_loop.start()


# One off
# def perspective_thread(manager, table):
#     """Perspective application thread starts its own tornado IOLoop, and
#     adds the table with the name "data_source_one", which will be used
#     in the front-end."""
#     psp_loop = tornado.ioloop.IOLoop()
#     manager.host_table("data_source_one", table)
#     if IS_MULTI_THREADED:
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             manager.set_loop_callback(psp_loop.run_in_executor, executor)
#             psp_loop.start()
#     else:
#         manager.set_loop_callback(psp_loop.add_callback)
#         psp_loop.start()


def make_app():
    data = get_data()
    table = Table(data)
    manager = PerspectiveManager()
    thread = threading.Thread(target=perspective_thread, args=(manager, table))
    thread.daemon = True
    thread.start()

    return tornado.web.Application(
        [
            (
                r"/websocket",
                PerspectiveTornadoHandler,
                {"manager": manager, "check_origin": False},
            ),
            (
                r"/node_modules/(.*)",
                tornado.web.StaticFileHandler,
                {"path": "../../node_modules/"},
            ),
            (
                r"/(.*)",
                tornado.web.StaticFileHandler,
                {"path": "./", "default_filename": "index.html"},
            ),
        ]
    )


def get_data():
    return pd.DataFrame(
        {
            "int": np.arange(20),
            "float": [i * 1.5 for i in range(20)],
            "bool": [True for _ in range(20)],
            "date": [date.today() for _ in range(20)],
            "datetime": [datetime.now() for _ in range(20)],
            "string": [str(i) for i in range(20)],
        }
    )


if __name__ == "__main__":
    try:
        app = make_app()
        app.listen(8080)
        logging.critical("Listening on http://localhost:8080")
        loop = tornado.ioloop.IOLoop.current()
        loop.start()
    except Exception:
        print(traceback.format_exc())
