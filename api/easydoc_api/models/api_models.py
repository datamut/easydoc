from enum import Enum

from pydantic import BaseModel


class ResponseStatus(Enum):
    SUCCESS = 'success'
    FAILED = "failed"


class BaseResponse(BaseModel):
    status: ResponseStatus
