import sys, subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))

suites=[
 "production_validation/pv05_semantic_calibration/test_pv05_semantic_calibration.py",
 "production_validation/pv02_failure_injection/test_pv02_failure_injection.py",
 "production_validation/pv03_recovery/test_pv03_recovery.py",
 "production_validation/pv04_load/test_pv04_load.py",
]
passed=0
for suite in suites:
    p=subprocess.run([sys.executable,suite],cwd=Path(__file__).resolve().parents[2],capture_output=True,text=True)
    print(f"SUITE {suite} EXIT={p.returncode}")
    print(p.stdout)
    if p.stderr: print(p.stderr)
    passed += p.returncode==0
assert passed==len(suites), f"{passed}/{len(suites)} suites passed"
print(f"PASS | PV05 integrated regression | {passed}/{len(suites)} suites")
