#!/usr/bin/env python3
"""Opt-in x402 v2 checkout for the fixed workflow-readiness fixture.

The buyer supplies and controls the EVM account through BUYER_PRIVATE_KEY.
This example never creates, stores, prints, or transmits that key directly.
"""

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
