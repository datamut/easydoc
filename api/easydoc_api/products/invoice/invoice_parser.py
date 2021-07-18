from typing import List

from easydoc_api.models.models import InvoiceInfo, InvoiceItem, Invoice, generate_invoice_id


def parse_invoice_items(invoice_id: str, raw_invoice: dict) -> List[InvoiceItem]:
    raw_items = []
    line_items = raw_invoice.get('invoice.lineitems', [])
    for tb in line_items:
        columns = [it.get('type') if it else 'n/a' for it in tb.get('types', [])]
        num_cols = len(columns)

        items = []
        for row in tb.get('cells', []):
            item = [it.get('text') if it else None for it in row]
            items.append(item)

        for it in items:
            if num_cols == len(it):
                raw_items.append(dict(zip(columns, it)))

    invoice_items: List[InvoiceItem] = []
    for item in raw_items:
        name = ' '.join([item.get('sypht.invoice.lineitems.id', ''),
                         item.get('sypht.invoice.lineitems.description', '')]).strip()
        sub_total = item.get('sypht.invoice.lineitems.subTotal')
        if sub_total is None:
            sub_total = item.get('sypht.invoice.lineitems.total')
        if sub_total is None or name is None:
            continue

        if sub_total.startswith('$'):
            sub_total = sub_total[1:]

        invoice_items.append(InvoiceItem(invoice_id=invoice_id, item_name=name, sub_total=sub_total))

    return invoice_items


def parse_invoice(raw_invoice: dict) -> Invoice:
    issuer_name = raw_invoice.get('issuer.name')
    issuer_address = raw_invoice.get('issuer.address')
    recipient_name = raw_invoice.get('recipient.name')
    document_date = raw_invoice.get('document.date')
    payment_date = raw_invoice.get('invoice.paymentDate')
    due_date = raw_invoice.get('invoice.dueDate')
    most_likely_currency = [k for k, v in raw_invoice.get('invoice.currencyCode', {}).items() if v.get('value') is True]
    currency = most_likely_currency[0].rsplit('.', 1)[-1] if most_likely_currency else None
    amount_due = raw_invoice.get('invoice.amountDue')
    amount_paid = raw_invoice.get('invoice.amountPaid')
    amount_tax = raw_invoice.get('invoice.tax')
    amount_total = raw_invoice.get('invoice.total')

    invoice_id = generate_invoice_id()

    invoice_items = parse_invoice_items(invoice_id, raw_invoice)
    amount_sum = sum([it.sub_total for it in invoice_items])
    num_items = len(invoice_items)

    invoice_info = InvoiceInfo(
        invoice_id=invoice_id,
        issuer_name=issuer_name,
        issuer_address=issuer_address,
        recipient_name=recipient_name,
        document_date=document_date,
        payment_date=payment_date,
        due_date=due_date,
        currency=currency,
        amount_due=amount_due,
        amount_paid=amount_paid,
        amount_tax=amount_tax,
        amount_total=amount_total,
        amount_sum=amount_sum,
        num_items=num_items
    )

    return Invoice(info=invoice_info, items=invoice_items)
