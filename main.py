from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from DbContext import SessionLocal
from models import ProductParameters, TokenModel

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def verify_token(
    appCodeClient: str = Header(None),
    tokenClient: str = Header(None),
    db: Session = Depends(get_db),
):
    token = db.query(TokenModel).filter(TokenModel.token == tokenClient).first()
    appCode = db.query(TokenModel).filter(TokenModel.appCode == appCodeClient).first()

    if not appCode or not token:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/get_production_parameter_by_code/{code}")
async def get_param_by_code(
    code: str, db: Session = Depends(get_db), token: str = Depends(verify_token)
):
    param = db.query(ProductParameters).filter(ProductParameters.code == code).first()
    if param is None:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return {
        "id": param.id,
        "name": param.name,
        "code": param.code,
        "parentCode": param.parentCode,
        "parameterTypeId": param.parameterTypeId,
    }


@app.get("/get_parameters_by_name")
async def get_params_by_name(
    name: str, db: Session = Depends(get_db), token: str = Depends(verify_token)
):
    params = (
        db.query(ProductParameters)
        .filter(ProductParameters.name.ilike(f"%{name}%"))
        .all()
    )
    if not params:
        raise HTTPException(status_code=404, detail="Parameters not found")
    return [
        {
            "id": param.id,
            "name": param.name,
            "code": param.code,
            "parentCode": param.parentCode,
            "parameterTypeId": param.parameterTypeId,
        }
        for param in params
    ]


@app.get("/get_parameters_by_parent_code/{parentCode}")
async def get_params_by_parent_code(
    parentCode: str, db: Session = Depends(get_db), token: str = Depends(verify_token)
):
    params = (
        db.query(ProductParameters)
        .filter(ProductParameters.parentCode == parentCode)
        .all()
    )
    if not params:
        raise HTTPException(status_code=404, detail="Parameters not found")
    return [
        {
            "id": param.id,
            "name": param.name,
            "code": param.code,
            "parentCode": param.parentCode,
            "parameterTypeId": param.parameterTypeId,
        }
        for param in params
    ]
