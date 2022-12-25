import uvicorn

from core.app import setup_app

if __name__ == "__main__":
    print("http://127.0.0.1:8000/docs")
    uvicorn.run(app=setup_app())
