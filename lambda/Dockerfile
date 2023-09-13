FROM public.ecr.aws/lambda/python:3.11

WORKDIR /app
COPY . ./

COPY app ${LAMBDA_TASK_ROOT}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip3 install poetry; \
    poetry export --without-hashes --output requirements.txt; \
    pip3 install -r requirements.txt

CMD ["index.handler"]
