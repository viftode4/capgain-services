import os
from pathlib import Path
import subprocess
import sys
from base64 import urlsafe_b64encode
import importlib.util
import json

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "buy_workflow_readiness.py"


def load_example():
    spec = importlib.util.spec_from_file_location("buy_workflow_readiness", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def encoded_challenge(module, **term_overrides):
    terms = dict(module.EXPECTED_TERMS)
    terms.update(term_overrides)
    challenge = {
        "x402Version": 2,
        "resource": {"url": module.URL},
        "accepts": [terms],
    }
    return urlsafe_b64encode(json.dumps(challenge).encode()).decode().rstrip("=")


def test_accepts_only_exact_approved_route_terms():
    module = load_example()
    challenge = module.decode_payment_required(encoded_challenge(module))
    module.validate_terms(challenge)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("amount", "10001"),
        ("network", "eip155:1"),
        ("asset", "0x0000000000000000000000000000000000000000"),
        ("payTo", "0x0000000000000000000000000000000000000000"),
    ],
)
def test_rejects_mismatched_payment_terms(field, bad_value):
    module = load_example()
    challenge = module.decode_payment_required(
        encoded_challenge(module, **{field: bad_value})
    )
    with pytest.raises(SystemExit, match="unexpected payment terms"):
        module.validate_terms(challenge)


def test_rejects_different_resource_url():
    module = load_example()
    challenge = module.decode_payment_required(encoded_challenge(module))
    challenge["resource"]["url"] = "https://example.invalid/other"
    with pytest.raises(SystemExit, match="different resource URL"):
        module.validate_terms(challenge)


@pytest.mark.parametrize("exact_first", [True, False])
def test_rejects_exact_option_mixed_with_an_extra_option(exact_first):
    module = load_example()
    challenge = module.decode_payment_required(encoded_challenge(module))
    extra = dict(module.EXPECTED_TERMS)
    extra["amount"] = "999999"
    extra["payTo"] = "0x0000000000000000000000000000000000000001"
    exact = challenge["accepts"][0]
    challenge["accepts"] = [exact, extra] if exact_first else [extra, exact]
    with pytest.raises(SystemExit, match="multiple payment options"):
        module.validate_terms(challenge)
