from fastapi.security import OAuth2PasswordBearer
from modules.database import Database

oauth2_scheme_dependency = OAuth2PasswordBearer(tokenUrl="user/token")


async def session_dependency():
    """Dependency for session management in functions."""
    async with Database.get_database().session_maker() as sess:
        yield sess
