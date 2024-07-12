from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Praktyk!234@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/get_production_parameter_by_code/{code}")
async def GetParamByCode(code: str, db: Session = Depends(get_db)):
    param = db.query(productParameters).filter(productParameters.code == code).first()
    if param is None:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return {
        "id": param.id,
        "name": param.name,
        "code": param.code,
        "parentCode": param.parentCode,
        "parameterTypeId": param.parameterTypeId
    }

@app.get("/get_parameters_by_name")
async def GetParamsByName(name: str, db: Session = Depends(get_db)):
    params = db.query(productParameters).filter(productParameters.name.ilike(f"%{name}%")).all()
    if params is None:
        raise HTTPException(status_code=404, detail="Parameters not found")
    return [
        {
            "id": param.id,
            "name": param.name,
            "code": param.code,
            "parentCode": param.parentCode,
            "parameterTypeId": param.parameterTypeId
        }
        for param in params
    ]

@app.get("/get_parameters_by_parent_code/{parentCode}")
async def GetParamsByParentCode(parentCode: str, db: Session = Depends(get_db)):
    params = db.query(productParameters).filter(productParameters.parentCode == parentCode).all()
    if params is None:
        raise HTTPException(status_code=404, detail="Parameters not found")
    return [
        {
            "id": param.id,
            "name": param.name,
            "code": param.code,
            "parentCode": param.parentCode,
            "parameterTypeId": param.parameterTypeId
        }
        for param in params
    ]