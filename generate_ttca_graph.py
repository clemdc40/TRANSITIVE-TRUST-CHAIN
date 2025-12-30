import json

principals = []
capabilities = []
edges = []

# Charger IAM brut
with open("iam_raw.json", "r") as f:
    data = json.load(f)

# --------------------
# 1. PRINCIPALS
# --------------------

# Users → Principals
for user in data["users"]:
    principals.append({
        "id": user["id"],
        "type": "Principal",
        "controlled": user["id"] == "user_james"  # attaquant initial
    })

# Roles → Principals
for role in data["roles"]:
    principals.append({
        "id": role["id"],
        "type": "Principal",
        "controlled": False
    })

# --------------------
# 2. CAPABILITIES
# --------------------

for policy in data["policies"]:
    capabilities.append({
        "id": policy["id"],
        "critical": policy["critical"]
    })

# --------------------
# 3. EDGES : CAN_ACT_AS
# --------------------

# Users → Roles (can_assume_roles)
for user in data["users"]:
    for role_id in user.get("can_assume_roles", []):
        edges.append({
            "from": user["id"],
            "to": role_id,
            "type": "CAN_ACT_AS"
        })

# Roles → Roles (trusted_by)
for role in data["roles"]:
    for trusted_entity in role.get("trusted_by", []):
        edges.append({
            "from": trusted_entity,
            "to": role["id"],
            "type": "CAN_ACT_AS"
        })

# --------------------
# 4. EDGES : HAS_CAPABILITY
# --------------------

for role in data["roles"]:
    for policy_id in role.get("policies", []):
        edges.append({
            "from": role["id"],
            "to": policy_id,
            "type": "HAS_CAPABILITY"
        })

# --------------------
# 5. EXPORT TTCA GRAPH
# --------------------

ttca_graph = {
    "principals": principals,
    "capabilities": capabilities,
    "edges": edges
}

with open("ttca_graph_from_raw.json", "w") as f:
    json.dump(ttca_graph, f, indent=4)

print("[+] ttca_graph_from_raw.json généré avec succès")
