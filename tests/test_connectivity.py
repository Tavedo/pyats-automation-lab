"""
test_connectivity.py
--------------------
End-to-end ping and reachability tests across the lab.
"""

from pyats import aetest

PING_MATRIX = [
    ("R1", "10.0.12.2"),   # R1 -> R2 Gi2
    ("R1", "10.0.13.2"),   # R1 -> R3 Gi2
    ("R2", "10.0.12.1"),   # R2 -> R1 Gi2
    ("R2", "10.0.23.2"),   # R2 -> R3 Gi3
    ("R3", "10.0.13.1"),   # R3 -> R1 Gi3
    ("R3", "10.0.23.1"),   # R3 -> R2 Gi3
    ("R1", "2.2.2.2"),     # R1 -> R2 Loopback (OSPF)
    ("R1", "3.3.3.3"),     # R1 -> R3 Loopback (OSPF)
    ("R2", "1.1.1.1"),     # R2 -> R1 Loopback (OSPF)
    ("R2", "3.3.3.3"),     # R2 -> R3 Loopback (OSPF)
    ("R1", "172.21.1.24"), # R1 -> c8 management
]


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_devices(self, testbed):
        for device in testbed.devices.values():
            device.connect(log_stdout=False)


class TestConnectivity(aetest.Testcase):
    @aetest.test
    def test_ping_matrix(self, testbed):
        failed = []
        for src_device_name, dst_ip in PING_MATRIX:
            device = testbed.devices.get(src_device_name)
            if not device:
                continue
            try:
                result = device.ping(dst_ip, count=5)
                if "!" not in result:
                    failed.append(f"{src_device_name} -> {dst_ip}: FAILED")
                else:
                    pass
            except Exception as e:
                failed.append(f"{src_device_name} -> {dst_ip}: ERROR - {e}")
        if failed:
            self.failed("Connectivity failures:\n" + "\n".join(failed))
        else:
            self.passed(f"All {len(PING_MATRIX)} ping tests passed")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed):
        for device in testbed.devices.values():
            device.disconnect()
