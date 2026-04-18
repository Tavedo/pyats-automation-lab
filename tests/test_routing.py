"""
test_routing.py
---------------
pyATS test suite to validate routing tables across all lab routers.
"""

from pyats import aetest


EXPECTED_ROUTES = {
    "R1": ["10.0.12.0/30", "10.0.13.0/30", "1.1.1.1/32"],
    "R2": ["10.0.12.0/30", "10.0.23.0/30", "2.2.2.2/32"],
    "R3": ["10.0.13.0/30", "10.0.23.0/30", "3.3.3.3/32"],
    "c8": ["172.21.1.0/24"],
}


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_devices(self, testbed):
        for device in testbed.devices.values():
            device.connect(log_stdout=False)

    @aetest.subsection
    def learn_routing(self, testbed):
        self.parent.parameters["routing_data"] = {}
        for device_name, device in testbed.devices.items():
            routing = device.learn("routing")
            self.parent.parameters["routing_data"][device_name] = routing.info


class TestRoutingTable(aetest.Testcase):
    @aetest.setup
    def setup(self, routing_data):
        self.routing_data = routing_data

    @aetest.test
    def test_expected_routes_present(self):
        failed = []
        for device, expected_routes in EXPECTED_ROUTES.items():
            device_routes = str(self.routing_data.get(device, {}))
            for route in expected_routes:
                if route not in device_routes:
                    failed.append(f"{device}: missing route {route}")
        if failed:
            self.failed("Missing routes:\n" + "\n".join(failed))
        else:
            self.passed("All expected routes are present")

    @aetest.test
    def test_ospf_neighbors(self):
        """Verify OSPF is forming adjacencies on R1, R2, R3."""
        ospf_devices = ["R1", "R2", "R3"]
        failed = []
        for device_name in ospf_devices:
            device = None
            for d in self.parent.parameters.get("testbed", {}).devices.values():
                if d.name == device_name:
                    device = d
                    break
            if device is None:
                continue
            try:
                output = device.execute("show ip ospf neighbor")
                if "FULL" not in output:
                    failed.append(f"{device_name}: no OSPF FULL neighbors found")
            except Exception as e:
                failed.append(f"{device_name}: {e}")
        if failed:
            self.failed("OSPF neighbor issues:\n" + "\n".join(failed))
        else:
            self.passed("OSPF adjacencies are established")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed):
        for device in testbed.devices.values():
            device.disconnect()
