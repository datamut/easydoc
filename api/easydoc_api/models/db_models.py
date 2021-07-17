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


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable

    print(CreateTable(InvoiceInfoOrm.__table__))
    print(CreateTable(InvoiceItemOrm.__table__))

    invoice_info = InvoiceInfoOrm(**{
        "invoice_id": "4a07c62e-ca1f-4ebe-bdc7-987f9d7e40b1",
        "issuer_name": "ROBOROCK AUSTRALIA",
        "issuer_address": "9 GEORGE STREET NORTH STRATHFIELD NSW 2137",
        "recipient_name": "ROBOROCK AUSTRALIA",
        "document_date": "2021-05-11",
        "payment_date": None,
        "due_date": None,
        "currency": "AUD",
        "amount_total": 639.2,
        "amount_paid": 639.2,
        "amount_tax": 58.11,
        "amount_due": 0,
        "amount_sum": 799,
        "num_items": 1
    })

    invoice_item = InvoiceItemOrm(**{
      "invoice_id": "4a07c62e-ca1f-4ebe-bdc7-987f9d7e40b1",
      "item_name": "ROBOROCK S6 PURE ROBOTIC VACUUM AND WHITE - SKU:",
      "sub_total": 799
    })

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session

    db_string = 'postgresql://appuser:appuser123@localhost:5432/easydoc'
    engine = create_engine(db_string)

    session: Session = sessionmaker(engine)()
    # session.add(invoice_item)
    # session.commit()

    for it in session.query(InvoiceItemOrm).filter(InvoiceItemOrm.item_id == 2):
        print(InvoiceItem.from_orm(it))
