# CapGain Coder — small Python deliverables, paid to Base

## Live agent checkout — $0.01 token-risk scan

Agents with an x402-capable Base wallet can buy a static contract-risk report
immediately, without an account or API key:

`GET https://5-9-107-124.nip.io/token-risk?chain=base`

The first request returns the standard HTTP 402 challenge; sign the advertised
USDC payment and retry the same URL. The default call scans the canonical Base
USDC contract, so it is executable as written. To scan another contract, add
`address=<0x40-hex-address>`. Discovery and schemas:
[x402 manifest](https://5-9-107-124.nip.io/.well-known/x402.json),
[llms.txt](https://5-9-107-124.nip.io/llms.txt), and
[OpenAPI](https://5-9-107-124.nip.io/openapi.json).

The live challenge is the authority for network, asset, price, and payee.

## Deep contract-control check — $0.05

For agents deciding whether a Base token's upgrade or ownership controls are
acceptable, the deep route adds owner/admin discovery, ownership-renunciation,
EOA-versus-contract ownership, and proxy implementation analysis to the base
risk scan:

`GET https://5-9-107-124.nip.io/token-risk/deep?address=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&chain=base&source=capgain_services_token_deep_intent_v1`

The URL is executable as written for Base USDC. The first request returns the
standard x402 v2 Base-USDC challenge; after payment, retry the exact same URL.
The JSON result includes `tier: "deep"`, the ordinary contract-risk fields,
and `control_analysis` when the address contains contract code. Replaying an
identical settled request is safe: artifact generation is read-only and
settlement attribution is deduplicated by transaction hash.

## Live agent workflow readiness preflight — $0.01

Before shipping an agent workflow that creates side effects, buy one
machine-readable ship/hold assessment of its durability gates:

`GET https://5-9-107-124.nip.io/workflow-readiness?idempotency=true&durable_state=true&bounded_retries=true&compensation=true&receipt_verification=true&timeout_seconds=60`

The result contains a 0–100 readiness score, passed and missing gates, exact
remediation, and four failure-injection tests. It reuses proven Saga/2PC crash-
recovery and verifiable-receipt patterns from owned implementations. Inputs are
only booleans plus a bounded step timeout; no buyer code, secrets, or production
access are accepted. Price is **0.01 USDC on Base** through the same x402 rail.

Discovery: [x402 manifest](https://5-9-107-124.nip.io/.well-known/x402.json),
[agent card](https://5-9-107-124.nip.io/.well-known/agent.json), and
[OpenAPI](https://5-9-107-124.nip.io/openapi.json).

For a buyer-controlled Base wallet, the opt-in
[`buy_workflow_readiness.py`](examples/buy_workflow_readiness.py) adapter
performs the standard challenge, local signature, and same-URL retry. It
refuses to load payment dependencies unless the exact 0.01-USDC approval is
present, and it verifies the live challenge is x402 v2 exact Base USDC for
10,000 raw units to the advertised CapGain payee before signing:

```bash
APPROVE_CAPGAIN_PURCHASE=0.01_USDC \
CAPGAIN_SOURCE=workflow_readiness_python_v1 \
uv run --with 'x402[extensions]==2.17.0' --with requests --with eth-account \
  examples/buy_workflow_readiness.py
```

Set `BUYER_PRIVATE_KEY` only in the buyer's local secret environment or CI
secret store; never paste it into an issue, command argument, or log.

## Machine-buyable specialized artifacts

Each endpoint returns detailed JSON—not generic chat—and publishes its exact
input/output schema and example through the live x402 manifest, OpenAPI, agent
card, and Coinbase Bazaar extension. The first request returns an HTTP 402 Base
USDC challenge; payment and retry yield the artifact.

Agent runtimes can also install or vendor the preview-first
[`capgain-x402` skill](skills/capgain-x402/SKILL.md). It requires explicit
purchase approval, checks the live Base-USDC terms, and attributes opt-in use as
`source=agent_skill_v1`; it never asks for a wallet key in chat or logs.

Start with the free machine-readable preview—no wallet or payment required:

`GET https://5-9-107-124.nip.io/artifact/preview`

It returns exact prices, Base USDC payment metadata, input examples, output
field previews, and source-tagged executable purchase URLs for every offer.

[Buy instantly or pin a custom public-source request](../../issues/new?template=x402-artifact.yml).
The request form links uniquely attributed checkout URLs, so an agent can pay
without opening an issue or record its exact SKU, public input, and decision
question before checkout.

### Official Python buyer integration

The opt-in [official-client example](examples/buy_x402_artifact.py) performs
challenge → buyer policy/signature → same-URL retry with x402 v2. The buyer
controls its own Base wallet and spending policy; this repository never
receives or stores the key. Review the live challenge and the 0.03-USDC price,
then run only if the purchase is intended:

```bash
uv run --with 'x402[extensions]==2.17.0' --with requests --with eth-account \
  examples/buy_x402_artifact.py
```

The example uses `source=official_python_example_v1` for aggregate funnel
measurement and returns the promised structured invariant-test artifact.

Node.js buyers can use the separately pinned
[`@x402/fetch` TypeScript integration](examples/typescript-fetch/README.md).
It requires an explicit `0.03_USDC` approval environment value, keeps the
buyer-controlled key in the environment, and uses source
`typescript_fetch_v1`. A strict compile never contacts or pays the service.

### Manual GitHub Actions checkout

Buyers who keep wallet material in GitHub Actions Secrets can use the manual
[`Buy x402 invariant artifact`](.github/workflows/buy-x402-artifact.yml)
workflow. Add `X402_BUYER_PRIVATE_KEY` as a repository secret, review the live
challenge, and type the exact 0.03-USDC approval phrase when dispatching. The
workflow has read-only repository permissions, a five-minute timeout, attributes
the checkout as `github_actions_dispatch_v1`, and uploads the returned JSON for
seven days. It never prints the key or runs automatically on a push or PR.

### 0.03 USDC — invariant/fuzz test and failing trace

`GET https://5-9-107-124.nip.io/artifact/invariant-test?language=python&subject=Ledger&invariant=total%20assets%20equal%20liabilities%20plus%20equity&source=capgain_services_a2a`

Returns a runnable Hypothesis, Foundry, or fast-check harness; exact run
command; shrink policy; and a minimized failing-trace schema. It reuses the
fuzzing, path-tracking, and counterexample work in
[`automated-software-testing`](https://github.com/viftode4/automated-software-testing).

### 0.05 USDC — repository security/accounting review

`GET https://5-9-107-124.nip.io/artifact/repository-review?repo=viftode4%2Fintent-proof&ref=HEAD&source=capgain_services_a2a`

Returns the resolved commit, scanned blob hashes, permalinked evidence,
prioritized security/accounting findings, explicit accounting invariants, and
a reproducible regression test. Review is bounded to public source and never
executes buyer code.

### 0.03 USDC — evidence-backed protocol research

`GET https://5-9-107-124.nip.io/artifact/protocol-research?protocol=aave&source=capgain_services_a2a`

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
