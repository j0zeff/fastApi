from typing import Annotated, Union
from fastapi import Body, FastAPI, Depends, Form, HTTPException, Header, Request, Query
from sqlalchemy.orm import Session
from DbContext import SessionLocal
from models import ProductParameters, TokenModel, Users
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="C:\\Users\\praktykant2\\Desktop\\praktyka\\static"), name="static")

templates = Jinja2Templates(directory="templates")

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


async def verify_authorization_token(accessToken: str = Header(None), db: Session = Depends(get_db)):
    token = db.query(Users).filter(Users.access_token == accessToken).first()
    if not token:
        return RedirectResponse(url='/login')


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

@app.get('/login', response_class=HTMLResponse)
async def log_in(request: Request):
    return templates.TemplateResponse("LoginView.html", {"request": request})


@app.post('/login')
async def log_in(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if user and user.check_password(password):
        token = user.create_access_token()
        db.commit()
        return JSONResponse(content={"access_token": user.access_token, "token_type": "bearer"})
    else: 
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    

@app.get('/create_user', response_class=HTMLResponse)
async def create_user(request: Request):
    return templates.TemplateResponse("CreateUserView.html", {"request": request})

@app.post('/create_user')
async def create_user(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    existingUser = db.query(Users).filter(Users.username == username).first()
    if existingUser:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = Users(username=username)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{"message": "User created succsessfuly", "user_id": new_user.id}

@app.get('/get_all_product_params', response_class=HTMLResponse)
async def get_all_product_params(
        request: Request, 
        search: str = Query(None),  
        skip: int = Query(0, alias='n'), 
        limit: int = Query(10, alias='m'), 
        db: Session = Depends(get_db),
        auth: str = Depends(verify_authorization_token)):
    paramsCount = db.query(ProductParameters).count()
    
    if skip < 0:
        skip = 0
    
    if skip >= paramsCount:
        skip = max(0, paramsCount - limit)

    if search:
        params = db.query(ProductParameters).filter(ProductParameters.name.ilike(f"%{search}%")).all()
        if not params:
            raise HTTPException(status_code=404, detail="Parameters not found")
    else:
        params = db.query(ProductParameters).offset(skip).limit(limit).all()
    
    
    return templates.TemplateResponse("ProductParamsView.html", {"request": request, "params": params, "skip": skip, "limit": limit})