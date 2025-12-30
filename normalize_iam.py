import json

with open("iam_raw.json", "r") as f:
    data = json.load(f)

print("Principals : ")

for p in data["users"]:
    print("     ", p["id"])

for p in data["roles"]:
    print("     ", p["id"])

print()
print("CAN_ACT_AS")

for p in data["users"]:
    for q in p["can_assume_roles"]:
        print(p["id"], " CAN_ACT_AS ", q)

for p in data["roles"]:
    for q in p["trusted_by"]:
        print(q, " CAN_ACT_AS ", p["id"])

print()
print("HAS_CAPABILITY")

for p in data["roles"]:
    for y in p["policies"]:
        print(p["id"], " HAS_CAPABILITY ", y)