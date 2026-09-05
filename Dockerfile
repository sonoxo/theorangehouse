FROM python:3.12-alpine
WORKDIR /app
COPY pyproject.toml ./
COPY orangehouse ./orangehouse
RUN adduser -D -u 10001 orangehouse && pip install --no-cache-dir .
USER orangehouse
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q -O- http://127.0.0.1:8080/health || exit 1
CMD ["orangehouse","serve","--host","0.0.0.0","--port","8080"]
