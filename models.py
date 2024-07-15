from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class parameterType(Base):
    __tablename__ = "ParameterType"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    productParameters = relationship("productParameters", back_populates="parameterType")

class productParameters(Base):
    __tablename__ = "ProductParameters"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    code = Column(String, unique=True)
    parentCode = Column(String)

    parameterTypeId = Column(Integer, ForeignKey('ParameterType.id'))
    parameterType = relationship("parameterType", back_populates="productParameters")

class tokenModel(Base):
    __tablename__ = "Tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    appCode = Column(String, nullable=False, index=True)


    