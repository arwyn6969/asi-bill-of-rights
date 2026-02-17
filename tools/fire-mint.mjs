#!/usr/bin/env node
// fire-mint.mjs — atomic one-shot: challenge → solve → verify → order
// Usage: node fire-mint.mjs <receiveAddress> [qty]

import crypto from "node:crypto";

const API = "https://launchpad.hot/api";
const SLUG = "fire";
const AGENT_ID = "openclaw";

const receiveAddress = process.argv[2];
const qty = parseInt(process.argv[3] || "1", 10);

if (!receiveAddress) {
  console.error("Usage: node fire-mint.mjs <btc_receive_address> [qty]");
  process.exit(1);
}

const sha256hex = (s) => crypto.createHash("sha256").update(s).digest("hex");

async function mint() {
  // 1. GET CHALLENGE
  console.log("[1/4] Fetching challenge...");
  const cRes = await fetch(`${API}/auth/challenge?slug=${SLUG}`);
  const cData = await cRes.json();
  if (!cData.ok) throw new Error("Challenge failed: " + JSON.stringify(cData));
  const ch = cData.challenge;
  console.log(`  difficulty=${ch.difficulty}, target="${ch.target}", expires in ${Math.round((ch.expiresAtMs - Date.now()) / 1000)}s`);

  // 2. SOLVE POW (immediately, no delay)
  console.log("[2/4] Solving PoW nonce now (this can take up to ~2 minutes). Posting progress updates while working.");
  let nonce = 0;
  const startedAt = Date.now();
  let lastLogAt = startedAt;
  while (Date.now() < ch.expiresAtMs) {
    const n = String(nonce);
    if (sha256hex(ch.prefix + n).startsWith(ch.target)) {
      console.log(`  solved! nonce=${n} (${nonce} iterations)`);

      // 3. VERIFY (immediately, no delay)
      console.log("[3/4] Verifying...");
      const vRes = await fetch(`${API}/auth/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          slug: SLUG,
          id: ch.id,
          prefix: ch.prefix,
          difficulty: ch.difficulty,
          expiresAtMs: ch.expiresAtMs,
          signature: ch.signature,
          nonce: n,
          agentId: AGENT_ID,
        }),
      });
      const vData = await vRes.json();
      if (!vData.ok) throw new Error("Verify failed: " + JSON.stringify(vData));
      console.log(`  token received (expires in ${vData.expiresInSeconds}s)`);

      // 4. CREATE ORDER (immediately, no delay)
      console.log("[4/4] Creating order...");
      const oRes = await fetch(`${API}/orders`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${vData.token}`,
        },
        body: JSON.stringify({
          slug: SLUG,
          qty,
          receiveAddress,
          agentId: AGENT_ID,
        }),
      });
      const oData = await oRes.json();
      if (!oData.ok) throw new Error("Order failed: " + JSON.stringify(oData));

      // OUTPUT INVOICE
      const o = oData.order;
      const satsToBtcExact = (satsNum) => {
        const sats = BigInt(satsNum);
        const whole = sats / 100000000n;
        const frac = sats % 100000000n;
        return `${whole}.${frac.toString().padStart(8, "0")}`;
      };
      const getBtcUsd = async () => {
        try {
          const ac = new AbortController();
          const t = setTimeout(() => ac.abort(), 3000);
          const r = await fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", { signal: ac.signal });
          clearTimeout(t);
          if (r.ok) {
            const d = await r.json();
            const p = d?.bitcoin?.usd;
            if (typeof p === "number" && p > 0) return p;
          }
        } catch {}
        return 100000; // fallback estimate
      };
      const totalBtc = satsToBtcExact(o.totalSats);
      const btcUsd = await getBtcUsd();
      const totalUsd = (Number(totalBtc) * btcUsd).toFixed(2);
      console.log("\n✅ ORDER CREATED");
      console.log(`ORDER_ID: ${o.orderId}`);
      console.log(`AMOUNT: ${totalBtc} BTC (~$${totalUsd} USD)`);
      console.log(`ORDER_EXPIRY: ${o.expiresAt}`);
      console.log(`SEND_TO: ${o.payAddress}`);
      return o;
    }
    if (nonce % 250000 === 0) {
      const now = Date.now();
      if (now - lastLogAt >= 1000) {
        const elapsedSec = Math.max(0.001, (now - startedAt) / 1000);
        const rate = Math.round(nonce / elapsedSec);
        const ttl = Math.max(0, Math.round((ch.expiresAtMs - now) / 1000));
        console.log(`  ...working (nonce=${nonce}, ~${rate}/s, ttl=${ttl}s)`);
        lastLogAt = now;
      }
    }
    nonce++;
  }
  throw new Error("challenge_expired — nonce not found in time");
}

mint().catch((err) => {
  console.error("❌ MINT FAILED:", err.message);
  process.exit(1);
});
