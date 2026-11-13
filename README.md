# DeliverySeal

**Local-first material delivery, receipt, and quantity verification evidence sealer for field operators.**

Offline. Deterministic. Pay once. Compatible with QuantumGuard CONTRACT-v1 and the Operator Pages suite.

## Why DeliverySeal?

Material shortages, disputed quantities, damaged deliveries, and "it never arrived" claims cost operators time and money. Without contemporaneous, verifiable records of what was delivered, by whom, in what condition, and against which PO or ticket, claims fail.

DeliverySeal captures structured delivery records (supplier, PO/ticket, items, quantities, condition, receiver, media hashes) and seals them into a client-verifiable QuantumGuard evidence bundle.

- No SaaS. No subscription. Runs completely offline after key setup.
- Clients, owners, or auditors verify with free QuantumGuard verifier (`qg verify`).
- Deterministic: same inputs → same sealed pack.
- Pairs with DailySeal, ChangeOrderSeal, MediaSeal, and the rest of the Operator Pages suite.

## Quick Start

```bash
pip install cryptography

python3 src/deliveryseal.py --demo
python3 src/deliveryseal.py --json samples/delivery-001.json --out sealed-delivery.json
```

Verify:
```bash
qg verify sealed-delivery.json
```
Expected: **PASS**.

## What you can sell

| SKU       | Price | Includes                                      |
|-----------|-------|-----------------------------------------------|
| Operator  | $59   | CLI + sample templates + key setup guide + 1-year email support |
| Command   | $169  | + batch mode + CSV/HTML export + reseller rights |
| Agency    | $449  | + white-label + multi-site key management |

**Buy Operator Pack (test mode):** https://buy.stripe.com/test_aFa3cu9517h655egpaew807  
Contact danpennic@gmail.com for production / other SKUs.  
Repo: https://github.com/danpennic-sys/deliveryseal

Source free under Apache-2.0 OR MIT. Commercial packs sold separately.

## License

Apache-2.0 OR MIT
