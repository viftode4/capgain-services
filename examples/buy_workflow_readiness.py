#!/usr/bin/env python3
"""Opt-in x402 v2 checkout for the fixed workflow-readiness fixture.

The buyer supplies and controls the EVM account through BUYER_PRIVATE_KEY.
This example never creates, stores, prints, or transmits that key directly.
"""

from base64 import urlsafe_b64decode
import json
import os
import re


SOURCE = os.environ.get("CAPGAIN_SOURCE", "workflow_readiness_python_v1")
if not re.fullmatch(r"[a-z0-9_-]{1,48}", SOURCE):
    raise SystemExit("CAPGAIN_SOURCE must be a safe aggregate attribution slug")

URL = (
    "https://5-9-107-124.nip.io/workflow-readiness"
    "?idempotency=true&durable_state=true&bounded_retries=true"
    "&compensation=true&receipt_verification=true&timeout_seconds=60"
    f"&source={SOURCE}"
)

EXPECTED_TERMS = {
    "scheme": "exact",
    "network": "eip155:8453",
    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "amount": "10000",
    "payTo": "0xa600bD74CB55958A79B535b4741fD66681Fc3e8c",
}


def decode_payment_required(value: str) -> dict:
    padding = "=" * (-len(value) % 4)
    return json.loads(urlsafe_b64decode(value + padding))


def validate_terms(challenge: dict) -> None:
    if challenge.get("x402Version") != 2:
        raise SystemExit("Refusing unexpected x402 version")
    if challenge.get("resource", {}).get("url") != URL:
        raise SystemExit("Refusing challenge for a different resource URL")

    options = challenge.get("accepts")
    if not isinstance(options, list) or len(options) != 1:
        raise SystemExit("Refusing x402 challenge with multiple payment options")

    matching = []
    for option in options:
        if not isinstance(option, dict):
            raise SystemExit("Refusing malformed x402 payment option")
        normalized = dict(option)
        normalized["asset"] = str(normalized.get("asset", "")).lower()
        normalized["payTo"] = str(normalized.get("payTo", "")).lower()
        expected = dict(EXPECTED_TERMS)
        expected["asset"] = expected["asset"].lower()
        expected["payTo"] = expected["payTo"].lower()
        if all(str(normalized.get(key)) == value for key, value in expected.items()):
            matching.append(option)
    if len(matching) != 1:
        raise SystemExit("Refusing x402 challenge with unexpected payment terms")


def main() -> None:
    if os.environ.get("APPROVE_CAPGAIN_PURCHASE") != "0.01_USDC":
        raise SystemExit(
            "Review the live challenge, then set "
            "APPROVE_CAPGAIN_PURCHASE=0.01_USDC"
        )

    private_key = os.environ.get("BUYER_PRIVATE_KEY")
    if not private_key or not re.fullmatch(r"0x[0-9a-fA-F]{64}", private_key):
        raise SystemExit(
            "Set a buyer-controlled BUYER_PRIVATE_KEY as 0x + 64 hex chars"
        )

    import requests
    from eth_account import Account
    from x402 import x402ClientSync
    from x402.http.clients.requests import wrapRequestsWithPayment
    from x402.mechanisms.evm.exact.client import ExactEvmScheme

    preflight = requests.get(URL, timeout=30.0)
    if preflight.status_code != 402:
        raise SystemExit(f"Expected HTTP 402 preflight, got {preflight.status_code}")
    encoded = preflight.headers.get("payment-required")
    if not encoded:
        raise SystemExit("HTTP 402 response omitted payment-required")
    validate_terms(decode_payment_required(encoded))

    payment_client = x402ClientSync()
    payment_client.register(
        "eip155:8453", ExactEvmScheme(Account.from_key(private_key))
    )
    session = wrapRequestsWithPayment(requests.Session(), payment_client)
    response = session.get(URL, timeout=30.0)
    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    main()
