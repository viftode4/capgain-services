import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "buy_workflow_readiness.py"


def run_example(**environment: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(environment)
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )


def test_requires_exact_purchase_approval_before_loading_payment_dependencies():
    result = run_example()
    assert result.returncode != 0
    assert "APPROVE_CAPGAIN_PURCHASE=0.01_USDC" in result.stderr


def test_rejects_unsafe_attribution_source():
    result = run_example(CAPGAIN_SOURCE="unsafe/source")
    assert result.returncode != 0
    assert "safe aggregate attribution slug" in result.stderr


def test_requires_well_formed_buyer_controlled_key_after_approval():
    result = run_example(APPROVE_CAPGAIN_PURCHASE="0.01_USDC")
    assert result.returncode != 0
    assert "buyer-controlled BUYER_PRIVATE_KEY" in result.stderr


def test_script_pins_exact_route_terms():
    source = SCRIPT.read_text()
    assert "https://5-9-107-124.nip.io/workflow-readiness" in source
    assert "idempotency=true" in source
    assert "receipt_verification=true" in source
    assert '"eip155:8453"' in source
    assert '"0.01_USDC"' in source
