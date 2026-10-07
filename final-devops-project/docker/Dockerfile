FROM python:3.13-slim AS builder
WORKDIR /build
COPY application/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.13-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 NOTES_DB=/data/notes.db
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY application/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt     && rm -rf /wheels     && useradd --uid 10001 --create-home appuser     && mkdir /data && chown 10001:10001 /data
COPY --chown=10001:10001 application/app.py application/wsgi.py ./
COPY --chown=10001:10001 application/templates ./templates
USER 10001:10001
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--worker-tmp-dir", "/tmp", "--access-logfile", "-", "wsgi:app"]
