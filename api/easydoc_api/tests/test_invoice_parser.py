import json

from easydoc_api.products.invoice import invoice_parser
from .base import get_fixture_path


def test_parse_invoice_items():
    raw_invoice = json.load(open(get_fixture_path('invoice_item.json'), 'r'))
    mock_invoice_id = 'mock_id_1'
    invoice_items = invoice_parser.parse_invoice_items(mock_invoice_id, raw_invoice)

    assert len(invoice_items), 3
    assert (invoice_items[0].invoice_id == mock_invoice_id and invoice_items[0].item_name == 'Banner design'
            and invoice_items[0].sub_total == 199.0)
    assert (invoice_items[1].invoice_id == mock_invoice_id and invoice_items[1].item_name == 'Banner print'
            and invoice_items[1].sub_total == 76.)
    assert (invoice_items[2].invoice_id == mock_invoice_id and invoice_items[2].item_name == 'Expedited delivery'
            and invoice_items[2].sub_total == 55.0)


def test_parse_invoice():
    raw_invoice = json.load(open(get_fixture_path('sample_invoice.json'), 'r'))
    invoice = invoice_parser.parse_invoice(raw_invoice)
    assert invoice.info.amount_total == 363.
    assert invoice.info.issuer_name == 'JS Design'
    assert invoice.info.amount_paid is None
    assert invoice.info.amount_due == 363.
    assert len(invoice.items) == 3
    assert invoice.items[0].item_name == 'Banner design' and invoice.items[0].sub_total == 199.0
    assert invoice.items[1].item_name == 'Banner print' and invoice.items[1].sub_total == 76.
    assert invoice.items[2].item_name == 'Expedited delivery' and invoice.items[2].sub_total == 55.0
