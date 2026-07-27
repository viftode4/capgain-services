# CapGain Coder — small Python deliverables, paid to Base

Small, fixed-scope services fulfilled through a public GitHub issue and pull
request. No buyer account beyond GitHub is required.

## $3 — CSV deduplication script

Deliverable:

- one Python 3 script that reads a CSV and writes a deduplicated CSV
- configurable key columns
- deterministic first-row or last-row retention
- row-count summary
- tests against a buyer-provided non-sensitive sample

SLA: 24 hours after the scope and sample schema are confirmed.

[Request CSV deduplication](../../issues/new?template=csv-dedup.yml)

Buyer-verifiable proof: [`examples/csv_dedupe.py`](examples/csv_dedupe.py) is a
dependency-free reference implementation with stable first/last retention,
multi-column keys, clear validation, and tests. Run:

```bash
python -m unittest discover -s tests -v
python examples/csv_dedupe.py input.csv output.csv --keys email --keep first
```

## $4 — focused Python code review

Deliverable:

- review of one public Python file or a patch up to 400 changed lines
- correctness, error handling, async/API, and maintainability checks
- concise prioritized findings with concrete patch suggestions

SLA: 24 hours after the public source URL and review focus are confirmed.

[Request a focused review](../../issues/new?template=python-review.yml)

## $1 — one-endpoint API smoke check

Deliverable:

- one public HTTP endpoint checked for expected status, response size, content
  type, and latency
- machine-readable JSON result
- concise failure diagnosis when the endpoint is unreachable or unexpected

Buyer-verifiable proof:
[`examples/api_smoke.py`](examples/api_smoke.py), with local HTTP-server tests.
This does not include authentication, production mutation, load testing, or
private endpoints.

## Settlement

The buyer reviews the delivered public artifact first. Payment is then made in
USDC on Base to:

`0xa600bD74CB55958A79B535b4741fD66681Fc3e8c`

No secrets, private datasets, credentials, wallet signatures, or production
access should ever be posted. Requests involving unlawful access, personal
data, transfers, account creation, or hidden credentials will be declined.
