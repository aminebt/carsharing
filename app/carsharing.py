import uvicorn
import os 
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

from db import engine
from routers import cars

app = FastAPI(title="Car Sharing", docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/env/{MY_ENV_VAR}")
def demo_env(MY_ENV_VAR: str):
    return {"Hello": f"From: {os.environ.get(MY_ENV_VAR, 'No such env var')}"}


@app.get("/allenv")
def demo_env():
    return {key: value for key, value in os.environ.items()}


@app.get("/whereami")
def demo_cm():
    return {f"current directory: {os.getcwd()}"}


@app.get("/displayfile")
def display_file():
    file = os.environ.get("FILE_LOCATION")
    if not file:
        return {"error": "env var FILE_LOCATION not set"}
    path = Path(file)
    if path.is_file():
        with open(path, 'r') as f:
            return {"file location": file,
                    "file content": f.read()}
    else:
        return {"error": f"file {path} does not exist"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

app.include_router(cars.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
