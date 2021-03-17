FROM python:3.8

COPY requirements.txt .
RUN pip instsall -r requirements.txt

ARG API_URL
ARG AUTH_TOKENS

ENV API_URL API_URL
ENV AUTH_TOKENS AUTH_TOKENS

COPY . .
CMD python mine.py
