import logging

import uvicorn
from core.app import setup_app

app = setup_app()
logging.info(
    f"Swagger link: http://{app.settings.host}:{app.settings.port}{app.docs_url}"
)

if __name__ == "__main__":
    uvicorn.run(app=app, use_colors=True)
