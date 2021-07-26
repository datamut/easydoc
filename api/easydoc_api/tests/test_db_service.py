from unittest import mock
from datetime import date

from easydoc_api.services import db_service
from easydoc_api.models.models import InvoiceInfo, InvoiceItem


class MockSessionMaker:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add(self, *args, **kwargs):
        pass

    def commit(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        return (it for it in [('2021-07-20', 291.1), ('2021-07-22', 300), ('2021-07-23', 12.8)])


def init_mock_db_service():
    return db_service.DBService('localhost', 'mock_user', 'mock_password', 5432, 'mock_db')


def test_get_daily_expense():
    with mock.patch.object(db_service, 'sessionmaker', MockSessionMaker):
        service = init_mock_db_service()
        stats = service.get_daily_expense(date(2021, 7, 20), date(2021, 7, 28))
        assert len(stats) == 3
        assert stats[0].by_time == date(2021, 7, 20) and stats[0].total == 291.1
        assert stats[1].by_time == date(2021, 7, 22) and stats[1].total == 300
        assert stats[2].by_time == date(2021, 7, 23) and stats[2].total == 12.8


def test_save_invoice_info():
    with mock.patch.object(db_service, 'sessionmaker', MockSessionMaker):
        service = init_mock_db_service()
        service.save_invoice_info(InvoiceInfo(
            issuer_name='mock issuer',
            amount_total=123.1
        ))


def test_save_invoice_items():
    with mock.patch.object(db_service, 'sessionmaker', MockSessionMaker):
        service = init_mock_db_service()
        service.save_invoice_items([
            InvoiceItem(
                invoice_id='mock_invoice_id',
                item_name='mock item',
                sub_total='100.2'
            )
        ])
