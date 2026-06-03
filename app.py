import re
from fastapi import FastAPI, Request, Depends, HTTPException, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# Database imports
from database.db import engine, Base, get_db
import database.models
from database.models import User, Organization

# Schema and Security imports
from schemas.auth import IndividualRegister, OrganizationRegister, LoginSchema
from auth.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    verify_access_token
)
from utils.id_generator import generate_organization_id

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexgenOps")

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Utilities ---

def validate_password(password: str):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html"
)

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="register.html"
    )

@app.post("/register/individual")
def register_individual(data: IndividualRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if not validate_password(data.password):
        raise HTTPException(status_code=400, detail="Weak password")

    new_user = User(
        account_type="Individual",
        full_name=data.full_name,
        email=data.email,
        mobile=data.mobile,
        password_hash=hash_password(data.password),
        role="Individual"
    )
    db.add(new_user)
    db.commit()
    return {"success": True, "message": "Individual registered successfully"}

@app.post("/register/organization")
def register_organization(data: OrganizationRegister, db: Session = Depends(get_db)):
    existing_org = db.query(Organization).filter(
        Organization.official_email == data.official_email
    ).first()

    if existing_org:
        raise HTTPException(status_code=400, detail="Organization already exists")

    org_id = generate_organization_id(db)

    organization = Organization(
        organization_id=org_id,
        organization_name=data.organization_name,
        organization_type=data.organization_type,
        official_email=data.official_email,
        official_mobile=data.official_mobile,
        country=data.country,
        state=data.state,
        city=data.city,
        address=data.address
    )
    db.add(organization)

    owner = User(
        organization_id=org_id,
        account_type="Organization",
        full_name=data.owner_name,
        designation=data.designation,
        email=data.owner_email,
        mobile=data.owner_mobile,
        password_hash=hash_password(data.password),
        role="Owner"
    )
    db.add(owner)
    db.commit()

    return {
        "success": True, 
        "organization_id": org_id, 
        "message": "Organization registered successfully"
    }

@app.get("/login-page", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(data: LoginSchema, response: Response, db: Session = Depends(get_db)):
    # Fixed the indentation logic here
    if data.organization_id:
        user = db.query(User).filter(
            User.email == data.email,
            User.organization_id == data.organization_id
        ).first()
    else:
        user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.failed_attempts >= 5:
        raise HTTPException(status_code=403, detail="Account locked")

    if not verify_password(data.password, user.password_hash):
        user.failed_attempts += 1
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Reset failed attempts on success
    user.failed_attempts = 0
    db.commit()

    token = create_access_token({"email": user.email, "role": user.role})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="strict"
    )

    return {"success": True, "redirect": "/dashboard"}

@app.get("/dashboard")
def dashboard(request: Request, access_token: str = Cookie(None)):
    if not access_token:
        return RedirectResponse(url="/login-page")

    payload = verify_access_token(access_token)
    if not payload:
        return RedirectResponse(url="/login-page")

    return templates.TemplateResponse(
    request=request,
    name="dashboard.html",
    context={"user": payload}
    )

@app.get("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    # Usually, a logout should redirect the user back to home or login
    return RedirectResponse(url="/login-page")
