import json

with open("iam_raw.json", "r") as f:
    data = json.load(f)

print("Relations assume : ")
for p in data["users"]:
    print("Utilisateur : ", p["id"], " assume ", p["can_assume_roles"])

print()
print("Policies critiques : ")
for p in data["policies"]:
    if(p["critical"] == True):
        print("Critique : ", p["id"])

print()
print("Trusted by : ")
for p in data["roles"]:
    for q in p["trusted_by"]:
        print(q, " -> ", p["id"])