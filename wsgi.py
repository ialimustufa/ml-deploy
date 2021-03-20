# from main import app
# import os
# # web: gunicorn --bind 0.0.0.0:8080 wsgi:app
# if __name__ == "__main__":
#     app.run(debug=False if os.environ.get("PORT") else True, port= int(os.environ.get("PORT") or 8080))

import multiprocessing

import gunicorn.app.base

from app import app as handler_app
import os


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

# def handler_app(environ, start_response):
#     response_body = b'Works fine'
#     status = '200 OK'

#     response_headers = [
#         ('Content-Type', 'text/plain'),
#     ]

#     start_response(status, response_headers)

#     return [response_body]


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
    }
    # StandaloneApplication(handler_app, {"debug":False if os.environ.get("PORT") else True, "port": int(os.environ.get("PORT") or 8080)}).run()
    StandaloneApplication(handler_app, {"debug":False, "port": int(os.environ.get("PORT") or 8080)}).run()