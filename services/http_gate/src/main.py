
from wsgiref.simple_server import make_server

from config import Config
from app import App

if __name__ == __main__:
    cfg = Config()
    cfg.load()
    app = App(cfg)
    s = make_server(
        cfg["server"]["ip"],
        cfg["server"]["post"],
        app)
    s.serve_forever()
