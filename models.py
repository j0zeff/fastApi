import secrets
import string
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import bcrypt
from pydantic import BaseModel


class ParamDelete(BaseModel):
    param_id: int

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserDelete(BaseModel):
    user_id: int


class UserResponse(UserBase):
    id: int
    isDeleted: bool

    class Config:
        orm_mode = True


Base = declarative_base()


class ParameterType(Base):
    __tablename__ = "ParameterType"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    productParameters = relationship(
        "ProductParameters", back_populates="parameterType"
    )


class ProductParameters(Base):
    __tablename__ = "ProductParameters"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    code = Column(String, unique=True)
    parentCode = Column(String)
    isDeleted = Column(Boolean, server_default=text("FALSE"), nullable=False)

    parameterTypeId = Column(Integer, ForeignKey("ParameterType.id"))
    parameterType = relationship("ParameterType", back_populates="productParameters")

    def delete_param(self):
        self.isDeleted = True
        return self


class TokenModel(Base):
    __tablename__ = "Tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    appCode = Column(String, nullable=False, index=True)


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    isDeleted = Column(Boolean, server_default=text("FALSE"), nullable=False)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def create_access_token(self):
        alphabet = string.ascii_letters + string.digits
        self.access_token = "".join(secrets.choice(alphabet) for i in range(20))
        return self.access_token

    def delete_user(self):
        self.isDeleted = True
        return self

    def recover_user(self):
        self.isDeleted = True
        return self
