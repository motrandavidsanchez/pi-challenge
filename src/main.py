from fastapi import FastAPI
from starlette import status

from src.settings.config import APP_DESCRIPTION, DOCS_URL, APP_NAME, APP_VERSION
from src.character.router import router as router_character

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

app.include_router(router_character, prefix="/character", tags=["Character"])


@app.get(path="/root", status_code=status.HTTP_200_OK)
def root():
    return {"msg": "Connected to PI application"}

