from dataclasses import asdict
# from typing import Optional

import uvicorn
from fastapi import FastAPI

from app.database.conn import db
from app.common.config import conf
from app.routes import index


def create_app():
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

    app.include_router(index.router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
