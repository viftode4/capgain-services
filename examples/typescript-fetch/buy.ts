import { ExactEvmScheme } from "@x402/evm/exact/client";
import { wrapFetchWithPayment, x402Client } from "@x402/fetch";
import { privateKeyToAccount } from "viem/accounts";

const url = new URL(
  "https://viftode4-token-risk-402.loca.lt/artifact/invariant-test",
);
url.searchParams.set("language", "typescript");
url.searchParams.set("subject", "Ledger");
url.searchParams.set("invariant", "assets equal liabilities plus equity");
url.searchParams.set("source", "typescript_fetch_v1");

if (process.env.APPROVE_CAPGAIN_PURCHASE !== "0.03_USDC") {
  throw new Error(
    "Review the live challenge, then set APPROVE_CAPGAIN_PURCHASE=0.03_USDC",
  );
}

const privateKey = process.env.EVM_PRIVATE_KEY;
if (!privateKey || !/^0x[0-9a-fA-F]{64}$/.test(privateKey)) {
  throw new Error("Set a buyer-controlled EVM_PRIVATE_KEY as 0x + 64 hex chars");
}

const client = new x402Client();
client.register(
  "eip155:8453",
  new ExactEvmScheme(privateKeyToAccount(privateKey as `0x${string}`)),
);

const response = await wrapFetchWithPayment(fetch, client)(url, { method: "GET" });
if (!response.ok) {
  throw new Error(`Purchase failed with HTTP ${response.status}`);
}
console.log(JSON.stringify(await response.json(), null, 2));
