from fastapi import (
    Body,
    FastAPI,
    Depends,
    Form,
    HTTPException,
    Header,
    Request,
    Query,
    Cookie,
)
from sqlalchemy.orm import Session
from DbContext import SessionLocal
from models import (
    ProductParameters,
    TokenModel,
    Users,
    UserBase,
    UserDelete,
    UserCreate,
    ParamDelete
)
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return templates.TemplateResponse(
            "AccessDeniedView.html", {"request": request}, status_code=exc.status_code
        )
    return await request.app.default_exception_handler(request, exc)


async def verify_token(
    appCodeClient: str = Header(None),
    tokenClient: str = Header(None),
    db: Session = Depends(get_db),
):
    token = db.query(TokenModel).filter(TokenModel.token == tokenClient).first()
    appCode = db.query(TokenModel).filter(TokenModel.appCode == appCodeClient).first()

    if not appCode or not token:
        raise HTTPException(status_code=401, detail="Unauthorized")


def verify_authorization_token(
    access_token: str = Cookie(None), db: Session = Depends(get_db)
):
    print(access_token)
    if access_token == None:
        raise HTTPException(status_code=401, detail="Login failed")

    user = db.query(Users).filter(Users.access_token == access_token).first()

    print("user: ", user)
    print("auth: ", access_token)
    if not user:
        raise HTTPException(status_code=401, detail="Login failed")

    return user


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


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/login")


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


@app.get("/menu", response_class=HTMLResponse)
async def show_menu(
    request: Request, auth: Users = Depends(verify_authorization_token)
):
    return templates.TemplateResponse("MenuView.html", {"request": request})


@app.get("/get_users", response_class=HTMLResponse)
async def get_users(
    request: Request,
    search: str = Query(None),
    skip: int = Query(0, alias="n"),
    limit: int = Query(6, alias="m"),
    db: Session = Depends(get_db),
    auth: Users = Depends(verify_authorization_token),
):
    usersCount = db.query(Users).filter(Users.isDeleted == False).count()

    if skip < 0:
        skip = 0

    if skip >= usersCount:
        skip -= limit

    if search:
        users = (
            db.query(Users)
            .filter(Users.username.ilike(f"%{search}%"))
            .filter(Users.isDeleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        users = (
            db.query(Users)
            .filter(Users.isDeleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    return templates.TemplateResponse(
        "UsersView.html",
        {
            "request": request,
            "users": users,
            "skip": skip,
            "limit": limit,
            "search": search,
        },
    )


@app.post("/delete_user")
async def delete_user(
    request: Request,
    user: UserDelete = Body(),
    db: Session = Depends(get_db),
    auth: Users = Depends(verify_authorization_token),
):
    userToDelete = db.query(Users).filter(Users.id == user.user_id).first()

    if not userToDelete:
        raise HTTPException(404, detail="No such user")

    userToDelete.delete_user()
    db.commit()
    return
    # return templates.TemplateResponse("UsersView.html", {"request": request})
    # return RedirectResponse(url="/get_users")


@app.post("/delete_product_param")
async def delete_product_param(
    request: Request,
    param: ParamDelete = Body(),
    db: Session = Depends(get_db),
    auth: Users = Depends(verify_authorization_token),
):
    paramToDelete = db.query(ProductParameters).filter(ProductParameters.id == param.param_id).first()

    if not paramToDelete:
        raise HTTPException(404, detail="No such user")

    paramToDelete.delete_param()
    db.commit()
    return



@app.get("/login", response_class=HTMLResponse)
async def log_in(
    request: Request, access_token: str = Cookie(None), db: Session = Depends(get_db)
):
    if access_token == None:
        return templates.TemplateResponse("LoginView.html", {"request": request})

    user = (
        db.query(Users)
        .filter(Users.access_token == access_token)
        .filter(Users.isDeleted == False)
        .first()
    )

    if not user:
        return templates.TemplateResponse("LoginView.html", {"request": request})

    return RedirectResponse(url="/get_all_product_params")


@app.post("/login")
async def log_in(
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
    request: Request = None,
):
    user = (
        db.query(Users)
        .filter(Users.username == username)
        .filter(Users.isDeleted == False)
        .first()
    )
    if user and user.check_password(password):
        token = user.create_access_token()
        db.commit()
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(key="access_token", value=token, httponly=True, secure=True)
        return response
    else:
        return templates.TemplateResponse(
            "LoginView.html",
            {"request": request, "error": "Incorrect username or password"},
        )


@app.get("/create_user", response_class=HTMLResponse)
async def create_user(
    request: Request, auth: Users = Depends(verify_authorization_token)
):

    if not auth:
        return templates.TemplateResponse("AccessDeniedView.html", {"request": request})

    return templates.TemplateResponse("CreateUserView.html", {"request": request})


@app.post("/create_user")
async def create_user(
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
    request: Request = None,
):
    existingUser = db.query(Users).filter(Users.username == username).first()
    if existingUser:
        return templates.TemplateResponse(
            "CreateUserView.html",
            {"request": request, "error": "Username already registered"},
        )

    new_user = Users(username=username)
    new_user.set_password(password)
    new_user.create_access_token()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return templates.TemplateResponse(
        "CreateUserView.html",
        {"request": request, "success": "User created successfully"},
    )


@app.get("/get_all_product_params", response_class=HTMLResponse)
async def get_all_product_params(
    request: Request,
    search: str = Query(None),
    skip: int = Query(0, alias="n"),
    limit: int = Query(6, alias="m"),
    db: Session = Depends(get_db),
    user: Users = Depends(verify_authorization_token),
):

    print(request.cookies)

    paramsCount = db.query(ProductParameters).filter(ProductParameters.isDeleted == False).count()

    if skip < 0:
        skip = 0

    if skip >= paramsCount:
        skip -= limit

    if search:
        params = (
            db.query(ProductParameters)
            .filter(ProductParameters.name.ilike(f"%{search}%"))
            .filter(ProductParameters.isDeleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        params = db.query(ProductParameters).filter(ProductParameters.isDeleted == False).offset(skip).limit(limit).all()

    return templates.TemplateResponse(
        "ProductParamsView.html",
        {
            "request": request,
            "params": params,
            "skip": skip,
            "limit": limit,
            "search": search,
        },
    )
