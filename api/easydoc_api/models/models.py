from datetime import date
import uuid
from typing import Optional, List

from pydantic import BaseModel, Field


def generate_invoice_id():
    return str(uuid.uuid4())


class InvoiceInfo(BaseModel):
    invoice_id: str = Field(default_factory=generate_invoice_id)
    issuer_name: str
    issuer_address: Optional[str]
    recipient_name: Optional[str]
    document_date: Optional[date]
    payment_date: Optional[date]
    due_date: Optional[date]
    currency: Optional[str]
    amount_total: float
    amount_paid: Optional[float]
    amount_tax: Optional[float]
    amount_due: Optional[float]
    amount_sum: Optional[float]
    num_items: Optional[int]

    class Config:
        orm_mode = True


class InvoiceItem(BaseModel):
    invoice_id: str
    item_name: str
    sub_total: float

    class Config:
        orm_mode = True


class Invoice(BaseModel):
    info: InvoiceInfo
    items: List[InvoiceItem]
