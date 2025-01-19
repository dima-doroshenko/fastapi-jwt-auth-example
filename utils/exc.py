from fastapi import HTTPException, status

UnauthedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid username or password'
)
UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='User not found'
)
InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token is invalid'
)

InvalidTokenTypeException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid token type'
)

UserInactiveException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='User is inactive'
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token has expired'
)

ThisUsernameIsAlreadyTaken = HTTPException(
    status.HTTP_409_CONFLICT,
    detail='User with same username already exists'
)