import config
import uvicorn
from account.router import router as account_router
from address.router import router as address_router
from fastapi import FastAPI
from modules.database import Database
from user.router import router as user_router


async def startup():
    """App startup function."""
    database = Database.get_database()
    await database.initialize()


def build_app():
    """Build an app for later usage."""
    app = FastAPI(
        debug=config.DEBUG,
        title="Crypto API",
        description="REST API for generating valid cryptocurrency addresses and displaying them",
        version=config.VERSION,
        docs_url="/docs" if config.DEBUG else None,
        redoc_url=None,
        on_startup=[startup],
    )
    app.include_router(user_router)
    app.include_router(account_router)
    app.include_router(address_router)
    return app


app = build_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
