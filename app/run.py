import uvicorn
from main import setup_app

if __name__ == '__main__':
    uvicorn.run(app=setup_app())
