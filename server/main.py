import uvicorn
from fastapi import FastAPI

from routes import routers

app = FastAPI()

for router in routers:
    app.include_router(router)

uvicorn.run(app, host="127.0.0.1", port=8000)