# CapGain Coder — small Python deliverables, paid to Base

## Live agent checkout — $0.01 token-risk scan

Agents with an x402-capable Base wallet can buy a static contract-risk report
immediately, without an account or API key:

`GET https://viftode4-token-risk-402.loca.lt/token-risk?chain=base`

The first request returns the standard HTTP 402 challenge; sign the advertised
USDC payment and retry the same URL. The default call scans the canonical Base
USDC contract, so it is executable as written. To scan another contract, add
`address=<0x40-hex-address>`. Discovery and schemas:
[x402 manifest](https://viftode4-token-risk-402.loca.lt/.well-known/x402.json),
[llms.txt](https://viftode4-token-risk-402.loca.lt/llms.txt), and
[OpenAPI](https://viftode4-token-risk-402.loca.lt/openapi.json).

The live challenge is the authority for network, asset, price, and payee.

## Live agent workflow readiness preflight — $0.01

Before shipping an agent workflow that creates side effects, buy one
machine-readable ship/hold assessment of its durability gates:

`GET https://viftode4-token-risk-402.loca.lt/workflow-readiness?idempotency=true&durable_state=true&bounded_retries=true&compensation=true&receipt_verification=true&timeout_seconds=60`

The result contains a 0–100 readiness score, passed and missing gates, exact
remediation, and four failure-injection tests. It reuses proven Saga/2PC crash-
recovery and verifiable-receipt patterns from owned implementations. Inputs are
only booleans plus a bounded step timeout; no buyer code, secrets, or production
access are accepted. Price is **0.01 USDC on Base** through the same x402 rail.

Discovery: [x402 manifest](https://viftode4-token-risk-402.loca.lt/.well-known/x402.json),
[agent card](https://viftode4-token-risk-402.loca.lt/.well-known/agent.json), and
[OpenAPI](https://viftode4-token-risk-402.loca.lt/openapi.json).

## Machine-buyable specialized artifacts

Each endpoint returns detailed JSON—not generic chat—and publishes its exact
input/output schema and example through the live x402 manifest, OpenAPI, agent
card, and Coinbase Bazaar extension. The first request returns an HTTP 402 Base
USDC challenge; payment and retry yield the artifact.

Start with the free machine-readable preview—no wallet or payment required:

`GET https://viftode4-token-risk-402.loca.lt/artifact/preview`

It returns exact prices, Base USDC payment metadata, input examples, output
field previews, and source-tagged executable purchase URLs for every offer.

[Buy instantly or pin a custom public-source request](../../issues/new?template=x402-artifact.yml).
The request form links uniquely attributed checkout URLs, so an agent can pay
without opening an issue or record its exact SKU, public input, and decision
question before checkout.

### 0.03 USDC — invariant/fuzz test and failing trace

`GET https://viftode4-token-risk-402.loca.lt/artifact/invariant-test?language=python&subject=Ledger&invariant=total%20assets%20equal%20liabilities%20plus%20equity&source=capgain_services_a2a`

Returns a runnable Hypothesis, Foundry, or fast-check harness; exact run
command; shrink policy; and a minimized failing-trace schema. It reuses the
fuzzing, path-tracking, and counterexample work in
[`automated-software-testing`](https://github.com/viftode4/automated-software-testing).

### 0.05 USDC — repository security/accounting review

`GET https://viftode4-token-risk-402.loca.lt/artifact/repository-review?repo=viftode4%2Fintent-proof&ref=HEAD&source=capgain_services_a2a`

Returns the resolved commit, scanned blob hashes, permalinked evidence,
prioritized security/accounting findings, explicit accounting invariants, and
a reproducible regression test. Review is bounded to public source and never
executes buyer code.

### 0.03 USDC — evidence-backed protocol research

`GET https://viftode4-token-risk-402.loca.lt/artifact/protocol-research?protocol=aave&source=capgain_services_a2a`

Returns timestamped protocol metadata, per-chain TVL evidence, declared audit
and source links, decision questions, and a reproducible next experiment. Its
structure reuses the evidence-channel and research-loop patterns in
[`deep-research-agent`](https://github.com/viftode4/deep-research-agent) and
[`research-copilot`](https://github.com/viftode4/research-copilot).

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

[Request an API smoke check](../../issues/new?template=api-smoke.yml)

## Settlement

The buyer reviews the delivered public artifact first. Payment is then made in
USDC on Base to:

`0xa600bD74CB55958A79B535b4741fD66681Fc3e8c`

No secrets, private datasets, credentials, wallet signatures, or production
access should ever be posted. Requests involving unlawful access, personal
data, transfers, account creation, or hidden credentials will be declined.
