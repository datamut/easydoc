import json
import unittest
from unittest import mock

from fastapi.testclient import TestClient

from easydoc_api.models.db_models import ExpenseByTime
from .base import init_mock_env, get_fixture_path

init_mock_env()


class MockAIServiceError:
    # noinspection PyMethodMayBeStatic
    def extract_invoice(self, *args, **kwargs):
        raise ConnectionError('mock connection error')


class MockAIService:
    # noinspection PyMethodMayBeStatic
    def extract_invoice(self, *args, **kwargs):
        return json.load(open(get_fixture_path('sample_invoice.json'), 'r'))


class MockDBService:
    def save_invoice_info(self, *args, **kwargs):
        pass

    def save_invoice_items(self, *args, **kwargs):
        pass

    # noinspection PyMethodMayBeStatic
    def get_daily_expense(self, *args, **kwargs):
        return [ExpenseByTime(by_time=it[0], total=it[1])
                for it in [('2021-07-20', 291.1), ('2021-07-22', 300), ('2021-07-23', 12.8)]]


@mock.patch('easydoc_api.app.ai_service', MockAIService)
@mock.patch('easydoc_api.app.db_service', MockDBService)
class TestApp(unittest.TestCase):
    def setUp(self):
        from easydoc_api.app import app

        self.client = TestClient(app)

    def test_extract_invoice(self):
        with open(get_fixture_path('Sample_Invoice.pdf'), 'rb') as f:
            response = self.client.request('POST', '/extract_invoice', files={"file": f})
            assert response.status_code == 200
            body = response.json()
            assert body['info']['issuer_name'] == 'JS Design'
            assert body['info']['amount_total'] == 363.
            assert body['info']['amount_due'] == 363.
            assert len(body['items']) == 3
            assert body['items'][0]['item_name'] == 'Banner design' and body['items'][0]['sub_total'] == 199.0
            assert body['items'][1]['item_name'] == 'Banner print' and body['items'][1]['sub_total'] == 76.
            assert body['items'][2]['item_name'] == 'Expedited delivery' and body['items'][2]['sub_total'] == 55.0

    def test_save_invoice(self):
        response = self.client.request('POST', '/invoice', json={
            'info': {
                'issuer_name': 'mock issuer',
                'amount_total': 100.
            },
            'items': []
        })
        assert response.status_code == 200
        assert response.json()['status'] == 'success'

    def test_save_invoice_info(self):
        response = self.client.request('POST', '/invoice_info', json={
            'issuer_name': 'mock issuer',
            'amount_total': 101.
        })
        assert response.status_code == 200
        assert response.json()['status'] == 'success'

    def test_save_invoice_items(self):
        response = self.client.request('POST', '/invoice_items', json=[
            {
                'invoice_id': 'i1',
                'item_name': 'prod-1',
                'sub_total': 10.1
            },
            {
                'invoice_id': 'i2',
                'item_name': 'prod-2',
                'sub_total': 10.2
            }
        ])
        assert response.status_code == 200
        assert response.json()['status'] == 'success'

    def test_get_daily_expense(self):
        response = self.client.request('GET', '/stats/daily_expense?start_time=2021-07-20&end_time=2021-07-28')
        assert response.status_code == 200
        stats = response.json()
        assert len(stats) == 3
        assert stats[0]['by_time'] == '2021-07-20' and stats[0]['total'] == 291.1
        assert stats[1]['by_time'] == '2021-07-22' and stats[1]['total'] == 300
        assert stats[2]['by_time'] == '2021-07-23' and stats[2]['total'] == 12.8

    def test_health(self):
        response = self.client.request('GET', '/health')
        assert response.status_code == 200
        assert response.json() == 'ok'

    def test_home(self):
        response = self.client.request('GET', '/')
        assert response.status_code == 307
        assert response.is_redirect is True
        assert response.next.path_url == '/docs'


@mock.patch('easydoc_api.app.ai_service', MockAIServiceError)
@mock.patch('easydoc_api.app.db_service', MockDBService)
class TestUnhandledErrors(unittest.TestCase):
    def setUp(self):
        from easydoc_api.app import app

        self.client = TestClient(app)

    def test_unhandled_exception(self):
        with open(get_fixture_path('Sample_Invoice.pdf'), 'rb') as f:
            response = self.client.request('POST', '/extract_invoice', files={"file": f})
            assert response.status_code == 500
            assert 'error' in response.json() and 'mock connection error' in response.json()['error']
