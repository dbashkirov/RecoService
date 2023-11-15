import os
from dotenv import load_dotenv
import uvicorn

from service.api.app import create_app
from service.settings import get_config

config = get_config()
app = create_app(config)


if __name__ == "__main__":

    load_dotenv()
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", "8080"))

    uvicorn.run(app, host=host, port=port)
