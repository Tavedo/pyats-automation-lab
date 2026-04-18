"""
learn_interfaces.py
-------------------
Takes a Genie snapshot of all interfaces across lab devices
and saves to the snapshots/ directory.

Usage:
    python scripts/learn_interfaces.py --testbed testbed/testbed.yaml
"""

import os
import json
import argparse
from datetime import datetime
from genie.testbed import load


def main():
    parser = argparse.ArgumentParser(description="Learn and snapshot interface state")
    parser.add_argument("--testbed", default="testbed/testbed.yaml")
    parser.add_argument("--output", default="snapshots")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(args.output, f"interfaces_{timestamp}")
    os.makedirs(out_dir, exist_ok=True)

    testbed = load(args.testbed)

    for device_name, device in testbed.devices.items():
        print(f"[+] Connecting to {device_name}...")
        device.connect(log_stdout=False)
        print(f"[+] Learning interfaces on {device_name}...")
        interfaces = device.learn("interface")
        out_file = os.path.join(out_dir, f"{device_name}_interfaces.json")
        with open(out_file, "w") as f:
            json.dump(interfaces.info, f, indent=2, default=str)
        print(f"    Saved -> {out_file}")
        device.disconnect()

    print(f"\n✅ Snapshot complete: {out_dir}")


if __name__ == "__main__":
    main()
