FROM python:3.11-slim AS base

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app/
COPY ./requirements.txt /app/requirements.txt
RUN pip install --disable-pip-version-check -Ur requirements.txt

FROM python:3.11-slim

EXPOSE 2113

COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY src/main.py /app/
CMD ["python", "/app/main.py"]

