from datetime import date

from pydantic import BaseModel
from sqlalchemy import Column, String, CHAR, Date, NUMERIC, INTEGER, TIMESTAMP, BOOLEAN, ForeignKey, Sequence, Identity
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from easydoc_api.models.models import InvoiceInfo, InvoiceItem

Base = declarative_base()


class InvoiceInfoOrm(Base):
    __tablename__ = 'invoice_info'

    invoice_id = Column(CHAR(36), primary_key=True)
    issuer_name = Column(String, nullable=False)
    issuer_address = Column(String)
    recipient_name = Column(String)
    document_date = Column(Date)
    payment_date = Column(Date)
    due_date = Column(Date)
    currency = Column(CHAR(3))
    amount_total = Column(NUMERIC, nullable=False)
    amount_paid = Column(NUMERIC)
    amount_tax = Column(NUMERIC)
    amount_due = Column(NUMERIC)
    amount_sum = Column(NUMERIC)
    num_items = Column(INTEGER)
    create_date = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_date = Column(TIMESTAMP, nullable=False, server_onupdate=func.now(), server_default=func.now())
    deleted = Column(BOOLEAN, nullable=False, server_default='false')


class InvoiceItemOrm(Base):
    __tablename__ = 'invoice_item'

    item_id = Column(INTEGER, Identity(), primary_key=True, nullable=False)
    invoice_id = Column(CHAR(36), ForeignKey('invoice_info.invoice_id'))
    item_name = Column(String)
    sub_total = Column(NUMERIC)
    create_date = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_date = Column(TIMESTAMP, nullable=False, server_onupdate=func.now(), server_default=func.now())
    deleted = Column(BOOLEAN, nullable=False, server_default='false')


class ExpenseByTime(BaseModel):
    by_time: date
    total: float
