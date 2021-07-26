from datetime import date
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from easydoc_api.models.db_models import InvoiceInfoOrm, InvoiceItemOrm, ExpenseByTime
from easydoc_api.models.models import InvoiceInfo, InvoiceItem


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
        if not invoice_items:
            return

        with sessionmaker(self.engine)() as session:
            for item in invoice_items:
                session.add(InvoiceItemOrm(**item.dict()))
            session.commit()

    def get_daily_expense(self, start_time: date, end_time: date):
        """
        Statistic for getting the daily expense. As only document_date seems to be available for every invoice,
        use document_date as the time for now. Ideally this time should be the actual payment time.

        This expense is for already paid invoice, unpaid are not considered (again, use amount_due to indicate for now).

        :param start_time: The statistic start time, inclusive
        :param end_time: The statistic end time, inclusive
        :return: The stats data as a list
        """
        with sessionmaker(self.engine)() as session:
            cursor = session.execute(('SELECT '
                                      'document_date as by_time, sum(amount_total) as total '
                                      'FROM invoice_info '
                                      'WHERE '
                                      '(amount_due IS null OR amount_due = 0) '
                                      'and document_date >= :start_time '
                                      'and document_date <= :end_time '
                                      'GROUP BY document_date'),
                                     {'start_time': start_time, 'end_time': end_time})
            return [ExpenseByTime(by_time=it[0], total=it[1]) for it in cursor]
