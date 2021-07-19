from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


async def unhandled_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as ex:
        # TODO: debug only to return exception
        return JSONResponse(status_code=500, content={'error': f'Unknown exception {ex}'})


def app_settings(app: FastAPI):
    app.middleware('http')(unhandled_exceptions_middleware)

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
