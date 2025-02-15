from pydantic import BaseModel, Awaitable, NaiveBayes, PositiveFloat, AwareDatetime, NaiveDatetime


class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: PositiveFloat
    timestamp: AwareDatetime | NaiveDatetime