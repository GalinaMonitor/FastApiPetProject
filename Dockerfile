FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ADD . / market/
WORKDIR /market

RUN chmod +x deploy/wait-for-it.sh deploy/entrypoint.sh
RUN pip install -r requirements.txt

ENTRYPOINT deploy/entrypoint.sh  && python -m uvicorn market.app:app --host 0.0.0.0 --port 8000

