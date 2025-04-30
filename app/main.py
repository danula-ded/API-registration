from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from . import models, schemas, auth
from .database import get_db, engine
from .config import TRUSTED_ADMIN_EMAILS

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    
    # Check if the email is in the trusted admin list
    role = models.UserRole.ADMIN if user.email in TRUSTED_ADMIN_EMAILS else models.UserRole.USER
    
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        points=100,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "id": db_user.id,
        "email": db_user.email,
        "is_admin": db_user.role == models.UserRole.ADMIN,
        "balance": db_user.points
    }

@app.post("/login", response_model=schemas.Token)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(user_data.email, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_admin": current_user.role == models.UserRole.ADMIN,
        "balance": current_user.points
    }

@app.post("/transfer", response_model=schemas.TransferResponse)
def transfer_points(
    transfer: schemas.TransferRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.points < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient points")
    
    receiver = db.query(models.User).filter(models.User.id == transfer.to_user_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    current_user.points -= transfer.amount
    receiver.points += transfer.amount
    
    transaction = models.Transaction(
        amount=transfer.amount,
        sender_id=current_user.id,
        receiver_id=receiver.id
    )
    
    db.add(transaction)
    db.commit()
    return {
        "msg": "transfer successful",
        "new_balance": current_user.points
    }

@app.get("/balance", response_model=schemas.BalanceResponse)
def get_balance(current_user: models.User = Depends(auth.get_current_user)):
    return {"balance": current_user.points}

@app.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.points.desc()).limit(10).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "balance": user.points
        }
        for user in users
    ]

@app.post("/marketplace/create", response_model=schemas.MarketplaceOfferResponse)
def create_listing(
    listing: schemas.MarketplaceOfferCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.points < listing.price:
        raise HTTPException(status_code=400, detail="Insufficient points")
    
    db_listing = models.MarketplaceListing(
        title=listing.title,
        description=listing.description,
        points_required=listing.price,
        owner_id=current_user.id
    )
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return {
        "msg": "offer created",
        "offer_id": db_listing.id
    }

@app.post("/marketplace/accept", response_model=schemas.MarketplaceAcceptResponse)
def accept_listing(
    request: schemas.MarketplaceAcceptRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    listing = db.query(models.MarketplaceListing).filter(models.MarketplaceListing.id == request.offer_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    if listing.status != models.ListingStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Listing is not active")
    
    if current_user.points < listing.points_required:
        raise HTTPException(status_code=400, detail="Insufficient points")
    
    owner = db.query(models.User).filter(models.User.id == listing.owner_id).first()
    
    current_user.points -= listing.points_required
    owner.points += listing.points_required
    
    listing.status = models.ListingStatus.ACCEPTED
    
    transaction = models.Transaction(
        amount=listing.points_required,
        sender_id=current_user.id,
        receiver_id=owner.id
    )
    
    db.add(transaction)
    db.commit()
    return {"msg": "offer accepted"}

@app.post("/admin/assign", response_model=schemas.AdminAssignResponse)
def assign_admin(
    request: schemas.AdminAssignRequest,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role == models.UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="User is already an admin")
    
    user.role = models.UserRole.ADMIN
    db.commit()
    return {"msg": "user is now admin"}

@app.post("/admin/topup", response_model=schemas.AdminTopupResponse)
def topup_balance(
    request: schemas.AdminTopupRequest,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.points += request.amount
    db.commit()
    return {
        "msg": "user balance updated",
        "new_balance": user.points
    }
