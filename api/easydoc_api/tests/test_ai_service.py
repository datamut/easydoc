from unittest import mock
from typing import Dict
import tempfile

from easydoc_api.services import ai_service


class MockSyphtClient:
    def __init__(self, *args, **kwargs):
        pass

    # noinspection PyMethodMayBeStatic
    def upload(self, file, products, *args, **kwargs) -> str:
        return 'fileId-0001'

    # noinspection PyMethodMayBeStatic
    def fetch_results(self, file_id, *args, **kwargs) -> Dict:
        return {
            'issuer.name': 'mock issuer'
        }


def test_extract_invoice():
    with mock.patch.object(ai_service, 'SyphtClient', MockSyphtClient):
        service = ai_service.AIService('mock_id', 'mock_secret')
        invoice = service.extract_invoice(tempfile.SpooledTemporaryFile(max_size=1024))
        assert invoice.get('issuer.name') == 'mock issuer'
