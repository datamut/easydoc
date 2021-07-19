FROM python:3.8.11-alpine

RUN apk update && apk add build-base postgresql-dev musl-dev

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /code
RUN chown appuser:appgroup -R .

USER appuser
ADD --chown=appuser:appgroup easydoc_api app/easydoc_api
ADD --chown=appuser:appgroup requirements.txt app

WORKDIR /code/app

RUN python -m venv venv
ENV PATH "/code/app/venv/bin:$PATH"
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8087

CMD ["uvicorn", "easydoc_api.app:app", "--host=0.0.0.0", "--port=8087", "--reload"]
