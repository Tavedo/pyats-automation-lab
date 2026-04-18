"""
full_test_job.py
----------------
pyATS job file that runs all test suites in sequence.

Usage:
    pyats run job jobs/full_test_job.py --testbed-file testbed/testbed.yaml
"""

import os

def main(runtime):
    tests_dir = os.path.join(os.path.dirname(__file__), "..", "tests")

    runtime.tasks.run(
        testscript=os.path.join(tests_dir, "test_interfaces.py"),
        taskid="Interface Validation",
    )

    runtime.tasks.run(
        testscript=os.path.join(tests_dir, "test_routing.py"),
        taskid="Routing Validation",
    )

    runtime.tasks.run(
        testscript=os.path.join(tests_dir, "test_connectivity.py"),
        taskid="Connectivity Validation",
    )
