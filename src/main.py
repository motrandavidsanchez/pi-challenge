from fastapi import FastAPI
from starlette import status

from src.settings.config import APP_DESCRIPTION, DOCS_URL, APP_NAME, APP_VERSION

app = FastAPI(
    description=APP_DESCRIPTION,
    docs_url=DOCS_URL,
    redoc_url=None,
    swagger_ui_parameters={
        "docExpansion": "none"
    },
    title=APP_NAME,
    version=APP_VERSION,
    root_path="/api/v1"
)


@app.get(path="/root", status_code=status.HTTP_200_OK)
def root():
    return {"Connected to PI application"}

