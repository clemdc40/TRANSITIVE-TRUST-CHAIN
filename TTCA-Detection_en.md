# Transitive Trust Chain Abuse (Detection)

## Algorithm

```
INPUT: TTCA graph in JSON

Select all principals such that controlled = true

FOR EACH controlled principal P
    EXPLORE paths via CAN_ACT_AS
    FOR EACH path of length >= 2
        Q ← last principal of the path
        IF Q has a critical capability
            IF P does not possess this capability
                DETECT TTCA
            ELSE
                IGNORE (false positive)
```

## Code

The code used is located in **detector.py**.
```py
import json

# Load the TTCA graph
with open("ttca_graph_scenario_3.json", "r") as f:
    data = json.load(f)

principals = {p["id"]: p for p in data["principals"]}
capabilities = {c["id"]: c for c in data["capabilities"]}

# Build CAN_ACT_AS relations
can_act_as = {}
has_capability = {}

for edge in data["edges"]:
    if edge["type"] == "CAN_ACT_AS":
        can_act_as.setdefault(edge["from"], []).append(edge["to"])
    elif edge["type"] == "HAS_CAPABILITY":
        has_capability.setdefault(edge["from"], []).append(edge["to"])


def principal_has_critical_capability(principal_id):
    for cap_id in has_capability.get(principal_id, []):
        if capabilities.get(cap_id, {}).get("critical", False):
            return True
    return False


def dfs(start, current, path, visited):
    visited.add(current)
    path.append(current)

    # Check TTCA condition
    if len(path) >= 3 and principal_has_critical_capability(current):
        if not principal_has_critical_capability(start):
            print(" TTCA detected:", " → ".join(path))

    # Explore CAN_ACT_AS relations
    for nxt in can_act_as.get(current, []):
        if nxt not in visited:
            dfs(start, nxt, path.copy(), visited.copy())


# Starting point: controlled principals
for pid, p in principals.items():
    if p.get("controlled", False):
        dfs(pid, pid, [], set())
```
If we test it on scenario 1, it is detected as TTCA, which is good.
On scenario 2, it is not detected as TTCA.
However, on scenario 3, it is detected as TTCA.

So we will need to modify this: do not alert if a direct path exists.

```py
import json

# === Load the TTCA graph ===
with open("ttca_graph.json", "r") as f:
    data = json.load(f)

# Indexing objects
principals = {p["id"]: p for p in data["principals"]}
capabilities = {c["id"]: c for c in data["capabilities"]}

# Relations
can_act_as = {}
has_capability = {}

for edge in data["edges"]:
    if edge["type"] == "CAN_ACT_AS":
        can_act_as.setdefault(edge["from"], []).append(edge["to"])
    elif edge["type"] == "HAS_CAPABILITY":
        has_capability.setdefault(edge["from"], []).append(edge["to"])


# === Utility functions ===

def principal_has_critical_capability(principal_id):
    """
    Check if a principal has a critical capability
    """
    for cap_id in has_capability.get(principal_id, []):
        if capabilities.get(cap_id, {}).get("critical", False):
            return True
    return False


def has_direct_access(start, target):
    """
    Check if start can reach target in a single CAN_ACT_AS
    """
    return target in can_act_as.get(start, [])


# === DFS exploration ===

def dfs(start, current, path, visited):
    visited.add(current)
    path.append(current)

    # TTCA condition
    if len(path) >= 3 and principal_has_critical_capability(current):

        # False positive: capability already on the initial principal
        if principal_has_critical_capability(start):
            return

        # Edge case: direct access exists (transitivity not necessary)
        if has_direct_access(start, current):
            return

        print(" TTCA detected:", " → ".join(path))

    # Continue exploration
    for nxt in can_act_as.get(current, []):
        if nxt not in visited:
            dfs(start, nxt, path.copy(), visited.copy())


# === Entry point: controlled principals ===

for pid, p in principals.items():
    if p.get("controlled", False):
        dfs(pid, pid, [], set())

```

To reduce false positives, the detector checks that the critical capability is only reachable by transitivity. If an equivalent direct access exists between the initial principal and the critical principal, the transitive chain is considered redundant and the alert is ignored.


## Verbose

A verbose mode has been implemented to make the detector’s reasoning explicit. This mode details the explored paths, the critical capabilities reached, as well as the reasons for rejection (false positives, direct access), facilitating understanding and validation of results.
