from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from DbContext import SessionLocal
from models import productParameters, tokenModel

app = FastAPI()

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verifyToken(appCodeClient: str = Header(None), tokenClient: str = Header(None), db: Session = Depends(getDb)):
    token = db.query(tokenModel).filter(tokenModel.token == tokenClient).first()
    appCode = db.query(tokenModel).filter(tokenModel.appCode == appCodeClient).first()
    
    if not appCode or not token:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/get_production_parameter_by_code/{code}")
async def GetParamByCode(code: str, db: Session = Depends(getDb), token: str = Depends(verifyToken)):
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
async def GetParamsByName(name: str, db: Session = Depends(getDb), token: str = Depends(verifyToken)):
    params = db.query(productParameters).filter(productParameters.name.ilike(f"%{name}%")).all()
    if params is []:
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
async def GetParamsByParentCode(parentCode: str, db: Session = Depends(getDb), token: str = Depends(verifyToken)):
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
