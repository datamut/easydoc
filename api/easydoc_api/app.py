from typing import List
from datetime import date

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from easydoc_api.products.invoice.invoice_parser import parse_invoice
from easydoc_api.models.models import Invoice, InvoiceInfo, InvoiceItem
from easydoc_api.models.db_models import ExpenseByTime
from easydoc_api.services.ai_service import AIService
from easydoc_api.services.db_service import DBService
from easydoc_api.models.api_models import BaseResponse, ResponseStatus
from easydoc_api.config.config import app_config

app = FastAPI()

origins = [
    'http://localhost:4200'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_service = AIService(app_config.ai_client_id, app_config.ai_client_secret)
db_service = DBService(**app_config.db_config.dict())


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def home():
    """
    Redirect home page to API docs
    """
    return '/docs'


@app.get('/health', status_code=200)
async def health():
    """
    Health endpoint for liveness probe.
    """
    return 'ok'


@app.post('/extract_invoice', response_model=Invoice)
async def extract_invoice(file: UploadFile = File(...)):
    raw_invoice = ai_service.extract_invoice(file.file)
    return parse_invoice(raw_invoice)


@app.post('/invoice', response_model=BaseResponse)
async def save_invoice(request: Invoice):
    db_service.save_invoice_info(request.info)
    db_service.save_invoice_items(request.items)
    return BaseResponse(status=ResponseStatus.SUCCESS)


@app.post('/invoice_info', response_model=BaseResponse)
async def save_invoice_info(request: InvoiceInfo):
    db_service.save_invoice_info(request)
    return BaseResponse(status=ResponseStatus.SUCCESS)


@app.post('/invoice_items', response_model=BaseResponse)
async def save_invoice_items(request: List[InvoiceItem]):
    db_service.save_invoice_items(request)
    return BaseResponse(status=ResponseStatus.SUCCESS)


@app.get('/stats/daily_expense', response_model=List[ExpenseByTime])
async def get_daily_expense(start_time: date, end_time: date):
    return db_service.get_daily_expense(start_time, end_time)
