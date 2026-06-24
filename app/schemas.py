from pydantic import BaseModel, field_validator


class TransactionRequest(BaseModel):
    request_id: str
    user_id: str
    amount: float

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value

    @field_validator("request_id", "user_id")
    @classmethod
    def validate_strings(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value


class UserSummary(BaseModel):
    user_id: str
    total_amount: float
    total_points: int
    transaction_count: int


class RankingResponse(BaseModel):
    rank: int
    user_id: str
    score: int