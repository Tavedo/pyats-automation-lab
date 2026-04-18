"""
test_interfaces.py
------------------
pyATS test suite to validate interface states across all lab devices.
Usage:
    pyats run job jobs/full_test_job.py --testbed-file testbed/testbed.yaml
"""

from pyats import aetest
from genie.testbed import load


EXPECTED_INTERFACES = {
    "R1": {
        "GigabitEthernet1": {"oper_status": "up", "ipv4": "172.21.1.21"},
        "GigabitEthernet2": {"oper_status": "up", "ipv4": "10.0.12.1"},
        "GigabitEthernet3": {"oper_status": "up", "ipv4": "10.0.13.1"},
        "Loopback0":        {"oper_status": "up", "ipv4": "1.1.1.1"},
    },
    "R2": {
        "GigabitEthernet1": {"oper_status": "up", "ipv4": "172.21.1.22"},
        "GigabitEthernet2": {"oper_status": "up", "ipv4": "10.0.12.2"},
        "GigabitEthernet3": {"oper_status": "up", "ipv4": "10.0.23.1"},
        "Loopback0":        {"oper_status": "up", "ipv4": "2.2.2.2"},
    },
    "R3": {
        "GigabitEthernet1": {"oper_status": "up", "ipv4": "172.21.1.23"},
        "GigabitEthernet2": {"oper_status": "up", "ipv4": "10.0.13.2"},
        "GigabitEthernet3": {"oper_status": "up", "ipv4": "10.0.23.2"},
        "Loopback0":        {"oper_status": "up", "ipv4": "3.3.3.3"},
    },
    "c8": {
        "GigabitEthernet1": {"oper_status": "up", "ipv4": "172.21.1.24"},
        "Loopback0":        {"oper_status": "up", "ipv4": "8.8.8.8"},
    },
}


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_devices(self, testbed):
        for device_name, device in testbed.devices.items():
            device.connect(log_stdout=False)

    @aetest.subsection
    def learn_interfaces(self, testbed):
        self.parent.parameters["interface_data"] = {}
        for device_name, device in testbed.devices.items():
            intf = device.learn("interface")
            self.parent.parameters["interface_data"][device_name] = intf.info


class TestInterfaceStatus(aetest.Testcase):
    @aetest.setup
    def setup(self, interface_data):
        self.interface_data = interface_data

    @aetest.test
    def test_interface_oper_status(self):
        failed = []
        for device, interfaces in EXPECTED_INTERFACES.items():
            if device not in self.interface_data:
                self.failed(f"Device {device} not found in learned data")
            for intf_name, expected in interfaces.items():
                intf_data = self.interface_data[device].get(intf_name, {})
                oper = intf_data.get("oper_status", "unknown")
                if oper != expected["oper_status"]:
                    failed.append(f"{device} {intf_name}: expected {expected['oper_status']}, got {oper}")
        if failed:
            self.failed(f"Interface status failures:\n" + "\n".join(failed))
        else:
            self.passed("All interfaces are in expected state")

    @aetest.test
    def test_interface_ip_addresses(self):
        failed = []
        for device, interfaces in EXPECTED_INTERFACES.items():
            intf_data = self.interface_data.get(device, {})
            for intf_name, expected in interfaces.items():
                intf = intf_data.get(intf_name, {})
                ipv4 = intf.get("ipv4", {})
                if expected["ipv4"] not in str(ipv4):
                    failed.append(f"{device} {intf_name}: expected IP {expected['ipv4']}, got {ipv4}")
        if failed:
            self.failed("IP address mismatches:\n" + "\n".join(failed))
        else:
            self.passed("All interface IP addresses are correct")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed):
        for device in testbed.devices.values():
            device.disconnect()


if __name__ == "__main__":
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed-file", default="testbed/testbed.yaml")
    args, _ = parser.parse_known_args()

    testbed = loader.load(args.testbed_file)
    aetest.main(testbed=testbed)
