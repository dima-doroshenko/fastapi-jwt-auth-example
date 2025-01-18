from fastapi.security import OAuth2PasswordBearer

from config import settings

TOKEN_TYPE_FILED = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.auth.token_url
)
