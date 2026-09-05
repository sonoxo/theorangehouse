# 🟠 The Orange House

**Privacy-first economic intelligence and scenario planning for the XUNIA ecosystem.**

This first functional projection models transparent treasury or resource scenarios without connecting to wallets, placing trades, moving funds, or storing personal data.

> Scenario output is educational planning data—not financial advice or a market forecast.

## Launch

```bash
python -m orangehouse serve
```

Or run a projection directly:

```bash
python -m orangehouse project 10000 --monthly-flow 500 --annual-rate 0.05 --volatility 0.15 --months 24
```

## API

```bash
curl -s http://127.0.0.1:8080/v1/project -H 'content-type: application/json' -d '{"starting_value":10000,"monthly_flow":500,"annual_rate":0.05,"volatility":0.15,"months":24}'
```

| Route | Purpose |
|---|---|
| `GET /health` | Runtime heartbeat |
| `GET /ontology` | Semantic entities and relations |
| `POST /v1/project` | Baseline plus low/high stress band |

## Architecture

```mermaid
flowchart TD
 A[Scenario input] --> B[Validation control]
 B --> C[Projection engine]
 C --> D[Baseline timeline]
 C --> E[Stress band]
 D --> F[JSON API or CLI]
 E --> F
```

## Controls

- Local-first, dependency-free runtime
- No wallet keys, custody, trading, or transaction signing
- Strict request-size and field validation
- Deterministic, reproducible output
- Non-root Docker runtime and automated tests

## Verify

```bash
python -m unittest discover -s tests -v
python -m compileall -q orangehouse
```

Historic Monero meta documents remain as upstream reference material. New components live under `orangehouse/`, `ontology/`, `tests/`, and `.github/workflows/`.
