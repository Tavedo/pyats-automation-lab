"""
collect_configs.py
------------------
Backs up running configurations from all lab devices.

Usage:
    python scripts/collect_configs.py --testbed testbed/testbed.yaml
"""

import os
import argparse
from datetime import datetime
from genie.testbed import load


def main():
    parser = argparse.ArgumentParser(description="Backup running configs from all devices")
    parser.add_argument("--testbed", default="testbed/testbed.yaml")
    parser.add_argument("--output", default="snapshots/configs")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(args.output, timestamp)
    os.makedirs(out_dir, exist_ok=True)

    testbed = load(args.testbed)

    for device_name, device in testbed.devices.items():
        print(f"[+] Connecting to {device_name}...")
        device.connect(log_stdout=False)
        print(f"[+] Collecting running config from {device_name}...")
        config = device.execute("show running-config")
        out_file = os.path.join(out_dir, f"{device_name}_running_config.txt")
        with open(out_file, "w") as f:
            f.write(config)
        print(f"    Saved -> {out_file}")
        device.disconnect()

    print(f"\n✅ Config backup complete: {out_dir}")


if __name__ == "__main__":
    main()
