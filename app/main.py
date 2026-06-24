from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, engine
from . import models, schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Reward System API",
    description="Backend service for transaction processing and user rewards",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home route
@app.get("/")
def home():
    return {
        "message": "Reward System API is running"
    }


# POST /transaction
@app.post("/transaction")
def create_transaction(
    transaction: schemas.TransactionRequest,
    db: Session = Depends(get_db)
):

    # Check duplicate request
    existing_transaction = db.query(models.Transaction).filter(
        models.Transaction.request_id == transaction.request_id
    ).first()

    if existing_transaction:
        raise HTTPException(
            status_code=400,
            detail="Duplicate request"
        )

    # Find user
    user = db.query(models.User).filter(
        models.User.user_id == transaction.user_id
    ).first()

    # Create user if not present
    if user is None:
        user = models.User(
            user_id=transaction.user_id,
            total_points=0,
            total_amount=0,
            transaction_count=0,
            penalty=0
        )
        db.add(user)

    # Calculate points
    points = int(transaction.amount // 10)

    # Create transaction record
    new_transaction = models.Transaction(
        request_id=transaction.request_id,
        user_id=transaction.user_id,
        amount=transaction.amount,
        points=points
    )

    try:
        # Update user totals
        user.total_amount += transaction.amount
        user.total_points += points
        user.transaction_count += 1

        # Basic abuse prevention
        if user.transaction_count > 5:
            user.penalty = 20

        # Save transaction
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Transaction failed:{str(e)}"
        )

    return {
        "message": "Transaction processed successfully",
        "points_added": points
    }


# GET /summary/{user_id}
@app.get("/summary/{user_id}", response_model=schemas.UserSummary)
def get_summary(user_id: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.user_id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# GET /ranking
@app.get("/ranking")
def get_ranking(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    ranking_list = []

    for user in users:
        score = (
            user.total_points
            + (user.transaction_count * 5)
            - user.penalty
        )

        ranking_list.append({
            "user_id": user.user_id,
            "score": score
        })

    # Sort descending by score
    ranking_list.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    result = []

    for i, user in enumerate(ranking_list):
        result.append({
            "rank": i + 1,
            "user_id": user["user_id"],
            "score": user["score"]
        })

    return result