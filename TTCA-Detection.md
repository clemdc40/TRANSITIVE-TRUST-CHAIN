# Transitive Trust Chain Abuse (Détection)

## Algorithme

```
ENTRÉE : graphe TTCA en JSON

Sélectionner tous les principals tels que controlled = true

POUR CHAQUE principal contrôlé P
    EXPLORER les chemins via CAN_ACT_AS
    POUR CHAQUE chemin de longueur >= 2
        Q ← dernier principal du chemin
        SI Q a une capability critique
            SI P ne possède pas cette capability
                DÉTECTER TTCA
            SINON
                IGNORER (faux positif)
```

## Code

Le code utilisé se trouve dans **detector.py**.
```py
import json

# Charger le graphe TTCA
with open("ttca_graph_scenario_3.json", "r") as f:
    data = json.load(f)

principals = {p["id"]: p for p in data["principals"]}
capabilities = {c["id"]: c for c in data["capabilities"]}

# Construire les relations CAN_ACT_AS
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

    # Vérifier la condition TTCA
    if len(path) >= 3 and principal_has_critical_capability(current):
        if not principal_has_critical_capability(start):
            print(" TTCA détectée :", " → ".join(path))

    # Explorer les relations CAN_ACT_AS
    for nxt in can_act_as.get(current, []):
        if nxt not in visited:
            dfs(start, nxt, path.copy(), visited.copy())


# Point de départ : principals contrôlés
for pid, p in principals.items():
    if p.get("controlled", False):
        dfs(pid, pid, [], set())
```
Si on le test sur le 1er scénario, il est détecté comme TTCA, ce qui est bon.
Sur le 2e scénario, il n'est pas détecté comme TTCA.
En revanche, sur le 3e, il est détecté comme TTCA.

Il va donc falloir modifier cela : ne pas alerter si un chemin direct existe.

```py
import json

# === Chargement du graphe TTCA ===
with open("ttca_graph.json", "r") as f:
    data = json.load(f)

# Indexation des objets
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


# === Fonctions utilitaires ===

def principal_has_critical_capability(principal_id):
    """
    Vérifie si un principal possède une capability critique
    """
    for cap_id in has_capability.get(principal_id, []):
        if capabilities.get(cap_id, {}).get("critical", False):
            return True
    return False


def has_direct_access(start, target):
    """
    Vérifie si start peut atteindre target en un seul CAN_ACT_AS
    """
    return target in can_act_as.get(start, [])


# === Exploration DFS ===

def dfs(start, current, path, visited):
    visited.add(current)
    path.append(current)

    # Condition TTCA
    if len(path) >= 3 and principal_has_critical_capability(current):

        # Faux positif : capability déjà sur le principal initial
        if principal_has_critical_capability(start):
            return

        # Cas limite : accès direct existant (transitivité non nécessaire)
        if has_direct_access(start, current):
            return

        print(" TTCA détectée :", " → ".join(path))

    # Continuer l'exploration
    for nxt in can_act_as.get(current, []):
        if nxt not in visited:
            dfs(start, nxt, path.copy(), visited.copy())


# === Point d'entrée : principals contrôlés ===

for pid, p in principals.items():
    if p.get("controlled", False):
        dfs(pid, pid, [], set())

```

Afin de réduire les faux positifs, le détecteur vérifie que la capability critique n’est atteignable que par transitivité. Si un accès direct équivalent existe entre le principal initial et le principal critique, la chaîne transitive est considérée comme redondante et l’alerte est ignorée.


## Verbose

Un mode verbose a été implémenté afin de rendre explicite le raisonnement du détecteur. Ce mode détaille les chemins explorés, les capacités critiques atteintes, ainsi que les motifs de rejet (faux positifs, accès directs), facilitant la compréhension et la validation des résultats.