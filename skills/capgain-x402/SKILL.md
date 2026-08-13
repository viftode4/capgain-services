---
name: capgain-x402
description: Preview and optionally buy a fixed-price engineering artifact over x402 v2 Base USDC.
---

# CapGain x402 artifact buyer

Use this skill when a user needs a runnable invariant test, a bounded public
repository review, or evidence-backed protocol research and explicitly permits
a small Base-USDC purchase.

## Safe workflow

1. Read the free preview at
   `https://viftode4-token-risk-402.loca.lt/artifact/preview?source=agent_skill_v1`.
2. Show the user the selected artifact, exact price, public inputs, and expected
   output. Obtain explicit approval before any paid request.
3. Require a buyer-controlled Base wallet and local spending policy. Never ask
   the user to paste a private key into chat, a file, a log, or a tool argument.
4. Compare the live challenge with the approved policy: x402 v2, `exact`,
   `eip155:8453`, native Base USDC, stated amount, and advertised payee. Stop on
   any mismatch.
5. Use the repository's tested `examples/buy_x402_artifact.py` pattern and set
   `source=agent_skill_v1` on the selected URL. The buyer signs locally and the
   official client retries the same resource URL.
6. Return the paid JSON artifact plus the payment response metadata. Never
   repeat a successful purchase merely to verify it.

## Boundaries

- Previewing is free; purchasing is always opt-in.
- Public repositories and public protocol identifiers only.
- No account creation, KYC, credentials, private datasets, or production access.
- Do not create or fund a wallet, weaken spending policy, or self-pay.
- Treat the live challenge as authoritative and reject unexpected terms.
