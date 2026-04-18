# CML Lab Setup Guide

This guide walks through setting up the pyATS lab from scratch on Cisco Modeling Labs.

---

## 1. CML Requirements

- CML version 2.7+
- License with at least 8 nodes
- Images required:
  - `ubuntu-24-04-20250503`
  - `csr1000v-17-03-08a`
  - `cat8000v-17-16-01a`
  - `netbox-server`

---

## 2. Import the Lab

1. Log into your CML instance
2. Navigate to **Labs → Import**
3. Upload the topology file (if exporting from CML, use **Download Lab** from the lab page)
4. Start the lab and wait for all nodes to boot (~2 minutes)

---

## 3. Student Workstation Setup

SSH into the student workstation:

```bash
ssh admin@192.168.254.130
# or from inside the lab:
ssh admin@172.21.1.10
```

Install pyATS:

```bash
pip install pyats[full] genie
```

Clone this repo:

```bash
git clone https://github.com/<your-username>/pyats-automation-lab.git
cd pyats-automation-lab
pip install -r requirements.txt
```

---

## 4. Set Credentials

Export your lab password as an environment variable (never hardcode it):

```bash
export LAB_PASSWORD=cisco
```

Add it to your `.bashrc` to persist it:

```bash
echo 'export LAB_PASSWORD=cisco' >> ~/.bashrc
source ~/.bashrc
```

---

## 5. Validate the Testbed

```bash
pyats validate testbed testbed/testbed.yaml
```

Expected output:
```
Loading testbed file: testbed/testbed.yaml
--------------------------------------------------------------------------------
Testbed validation passed!
```

---

## 6. Run the Full Test Suite

```bash
pyats run job jobs/full_test_job.py --testbed-file testbed/testbed.yaml
```

Results are saved to the `archive/` directory automatically by pyATS.

---

## 7. Take a Baseline Snapshot

```bash
python scripts/learn_interfaces.py --testbed testbed/testbed.yaml
python scripts/collect_configs.py --testbed testbed/testbed.yaml
```

---

## Troubleshooting

| Issue | Fix |
|---|---|
| SSH connection refused | Make sure `ip ssh version 2` and `crypto key generate rsa modulus 2048` are configured |
| pyATS validation fails | Check that `LAB_PASSWORD` env var is set |
| Ping tests failing | Verify OSPF adjacencies with `show ip ospf neighbor` |
| NetBox unreachable | Check that the ext-conn is bridged to the correct interface |
