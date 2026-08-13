#!/usr/bin/env python3
"""Opt-in x402 v2 buyer example for a CapGain artifact.

The buyer supplies and controls the EVM account through BUYER_PRIVATE_KEY.
This example never creates, stores, prints, or transmits that key directly.
"""

import os

import httpx
from eth_account import Account
from x402.clients.httpx import x402HttpxClient
from x402.mechanisms.evm.exact import ExactEvmScheme


URL = (
    "https://viftode4-token-risk-402.loca.lt/artifact/invariant-test"
    "?language=python&subject=Ledger"
    "&invariant=assets%20equal%20liabilities%20plus%20equity"
    "&source=official_python_example_v1"
)


def main() -> None:
    private_key = os.environ.get("BUYER_PRIVATE_KEY")
    if not private_key:
        raise SystemExit("Set BUYER_PRIVATE_KEY to a buyer-controlled Base wallet key")

    account = Account.from_key(private_key)
    client = x402HttpxClient(account=account, schemes=[ExactEvmScheme()])
    with httpx.Client(transport=client, timeout=30.0) as session:
        response = session.get(URL)
        response.raise_for_status()
        print(response.json())


if __name__ == "__main__":
    main()
