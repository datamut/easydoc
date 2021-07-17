from typing import List

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from easydoc_api.models.models import InvoiceInfo, InvoiceItem
from easydoc_api.models.db_models import InvoiceInfoOrm, InvoiceItemOrm


class DBService:

    _engine: Engine = None

    def __init__(self, host: str, user: str, password: str, port: int, db_name: str):
        if DBService._engine is None:
            db_string = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
            DBService._engine = create_engine(db_string)

    @property
    def engine(self) -> Engine:
        return self._engine

    def save_invoice_info(self, invoice_info: InvoiceInfo):
        with sessionmaker(self.engine)() as session:
            session.add(InvoiceInfoOrm(**invoice_info.dict()))
            session.commit()

    def save_invoice_items(self, invoice_items: List[InvoiceItem]):
        with sessionmaker(self.engine)() as session:
            for item in invoice_items:
                session.add(InvoiceItemOrm(**item.dict()))
            session.commit()
