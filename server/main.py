import logging

logging.basicConfig(level=logging.INFO, format = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s")
logger = logging.getLogger(__name__)

from dotenv import load_dotenv

logger.info("Loading environment variables...")
load_dotenv(".env", override=True)
logger.info("Loaded.")

import uvicorn
from fastapi import FastAPI

from routes import routers

app = FastAPI(
    title="sage",
    description="Sage API",
)

for router in routers:
    app.include_router(router)

for route in app.routes:
    logger.info(route)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)