# 🧪 pyATS Automation Lab

A network automation lab built on **Cisco Modeling Labs (CML)** using **pyATS/Genie** for automated testing, validation, and configuration management. This project demonstrates real-world network automation skills across IOS-XE routers (CSR1000v, Catalyst 8000v) integrated with NetBox as the source of truth.

---

## 📐 Lab Topology

```
                  Management Network: 172.21.1.0/24
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  [Student WS]──────┬──────[R1]──────[NetBox]                   │
│  172.21.1.10       │      172.21.1.21                          │
│                    │                                            │
│              [SW-MGMT]──[R2]──────[R3]──────[c8]              │
│                         .22        .23        .24              │
└─────────────────────────────────────────────────────────────────┘

Point-to-Point Links (Data Plane):
  R1 Gi2 ──── R2 Gi2   →  10.0.12.0/30  (.1 / .2)
  R1 Gi3 ──── R3 Gi2   →  10.0.13.0/30  (.1 / .2)
  R2 Gi3 ──── R3 Gi3   →  10.0.23.0/30  (.1 / .2)
```

| Device | Role | OS | Image | Mgmt IP |
|---|---|---|---|---|
| Student Workstation | Automation Controller | Ubuntu 24.04 | ubuntu-24-04-20250503 | 172.21.1.10 |
| R1 | Core Router | IOS-XE 17.3.8a | CSR1000v | 172.21.1.21 |
| R2 | Core Router | IOS-XE 17.3.8a | CSR1000v | 172.21.1.22 |
| R3 | Core Router | IOS-XE 17.3.8a | CSR1000v | 172.21.1.23 |
| c8 | Edge Router | IOS-XE 17.16.1a | Catalyst 8000v | 172.21.1.24 |
| NetBox | IPAM / Source of Truth | NetBox | netbox-server | DHCP |

---

## 📁 Project Structure

```
pyats-automation-lab/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .gitignore                  # Ignored files
│
├── testbed/
│   └── testbed.yaml            # pyATS testbed definition
│
├── configs/
│   ├── R1_config.txt           # Startup config for R1
│   ├── R2_config.txt           # Startup config for R2
│   ├── R3_config.txt           # Startup config for R3
│   └── c8_config.txt           # Startup config for c8
│
├── tests/
│   ├── test_interfaces.py      # Interface state validation
│   ├── test_routing.py         # Routing table validation
│   └── test_connectivity.py    # End-to-end ping tests
│
├── scripts/
│   ├── learn_interfaces.py     # Genie learn interfaces snapshot
│   ├── learn_routing.py        # Genie learn routing snapshot
│   └── collect_configs.py      # Backup running configs
│
├── jobs/
│   └── full_test_job.py        # pyATS job file (run all tests)
│
└── docs/
    └── setup.md                # CML setup guide
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Access to the CML instance with the pyATS lab running
- SSH access to the Student Workstation (`172.21.1.10`)

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/pyats-automation-lab.git
cd pyats-automation-lab
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify testbed connectivity
```bash
pyats validate testbed testbed/testbed.yaml
```

### 4. Run all tests
```bash
pyats run job jobs/full_test_job.py --testbed-file testbed/testbed.yaml
```

### 5. Learn device state (snapshot)
```bash
genie learn interface routing --testbed testbed/testbed.yaml \
  --devices R1 R2 R3 c8 --output snapshots/
```

---

## 🧪 Test Suites

### Interface Tests (`tests/test_interfaces.py`)
- Verifies all expected interfaces are up/up
- Checks IP addresses are correctly configured
- Validates no unexpected interfaces are down

### Routing Tests (`tests/test_routing.py`)
- Validates routing table entries exist for all p2p subnets
- Checks OSPF/static routes are present
- Verifies default route is advertised

### Connectivity Tests (`tests/test_connectivity.py`)
- End-to-end ping between all routers
- Loopback reachability checks
- Management plane reachability

---

## 📦 Technologies Used

| Tool | Purpose |
|---|---|
| [Cisco CML](https://www.cisco.com/c/en/us/products/cloud-systems-management/modeling-labs/index.html) | Network simulation platform |
| [pyATS](https://developer.cisco.com/pyats/) | Network test automation framework |
| [Genie](https://developer.cisco.com/docs/genie-docs/) | Network automation library (parsers, models) |
| [Unicon](https://pypi.org/project/unicon/) | Device connection library |
| [NetBox](https://netbox.dev/) | IPAM / Source of truth |
| [Python 3](https://www.python.org/) | Scripting language |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)
