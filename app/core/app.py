from fastapi import FastAPI


class Application(FastAPI):
    pass


app = Application()


def setup_app() -> "Application":
    return app
