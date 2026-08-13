# TypeScript fetch buyer

Opt-in Node.js 20+ integration using the official `@x402/fetch` and
`@x402/evm` packages. It buys one 0.03-USDC TypeScript invariant artifact on
Base and attributes aggregate funnel use as `typescript_fetch_v1`.

Review the live 402 challenge before opting in. The script refuses to sign
unless the exact approval value is present, takes the buyer-controlled key only
from the environment, and never prints or stores it.

```bash
npm install
EVM_PRIVATE_KEY=0x... APPROVE_CAPGAIN_PURCHASE=0.03_USDC npm run buy
```

`npm run check` performs a strict compile without payment.
