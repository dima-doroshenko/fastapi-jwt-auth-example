from typing_extensions import deprecated

from datetime import datetime

from database import UsersOrm


class UserProperties:
    obj: UsersOrm
    
    @property
    def id(self) -> int:
        return self.obj.id
    
    @property
    def username(self) -> str:
        return self.obj.username
    
    @property
    def email(self) -> str:
        return self.obj.email
    
    @property
    def is_active(self) -> bool:
        return self.obj.is_active
    
    @property
    def verified(self) -> bool:
        return self.obj.verified

    @property 
    def hashed_password(self) -> bytes:
        return self.obj.hashed_password
    
    @property
    def created_at(self) -> datetime:
        return self.obj.created_at
    
    @verified.setter
    def verified(self, value: bool) -> None:
        self.obj.verified = value

    @is_active.setter
    def is_active(self, value: bool) -> None:
        self.obj.is_active = value

    @username.setter
    @deprecated('Username must be edit via the user.set_username(...)')
    def username(self, value) -> None:
        raise NotImplementedError

    @email.setter
    @deprecated('Email must be edit via the user.set_email(...)')
    def email(self, value) -> None:
        raise NotImplementedError
    
    @hashed_password.setter
    @deprecated('Password must be edit via the user.set_password(...)')
    def hashed_password(self, value) -> None:
        raise NotImplementedError
    