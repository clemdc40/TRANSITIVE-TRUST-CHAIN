import json

# =====================
# CONFIGURATION
# =====================
VERBOSE = True  # Mettre False pour désactiver les logs explicatifs


def vprint(msg):
    if VERBOSE:
        print("[VERBOSE]", msg)


# =====================
# CHARGEMENT DU GRAPHE
# =====================
with open("ttca_graph_from_raw.json", "r") as f:
    data = json.load(f)

principals = {p["id"]: p for p in data["principals"]}
capabilities = {c["id"]: c for c in data["capabilities"]}

can_act_as = {}
has_capability = {}

for edge in data["edges"]:
    if edge["type"] == "CAN_ACT_AS":
        can_act_as.setdefault(edge["from"], []).append(edge["to"])
    elif edge["type"] == "HAS_CAPABILITY":
        has_capability.setdefault(edge["from"], []).append(edge["to"])


# =====================
# FONCTIONS UTILITAIRES
# =====================
def principal_has_critical_capability(principal_id):
    for cap_id in has_capability.get(principal_id, []):
        if capabilities.get(cap_id, {}).get("critical", False):
            return True
    return False


def has_direct_access(start, target):
    return target in can_act_as.get(start, [])


# =====================
# DFS TTCA
# =====================
def dfs(start, current, path, visited):
    visited.add(current)
    path.append(current)

    vprint(f"Exploration du chemin : {' → '.join(path)}")

    # ---- Condition TTCA ----
    if len(path) >= 3 and principal_has_critical_capability(current):
        vprint(f"Capability critique atteinte via {current}")

        # Faux positif : capability déjà accessible
        if principal_has_critical_capability(start):
            vprint(
                f"Chemin ignoré : la capability critique est déjà accessible depuis {start}"
            )
            return

        # Cas limite : accès direct existant
        if has_direct_access(start, current):
            vprint(
                f"Chemin ignoré : accès direct {start} → {current} détecté (transitivité non nécessaire)"
            )
            return

        # TTCA valide
        print("⚠️ TTCA détectée :", " → ".join(path))
        vprint("TTCA confirmée : la transitivité est nécessaire")

    # ---- Continuer l'exploration ----
    for nxt in can_act_as.get(current, []):
        if nxt not in visited:
            dfs(start, nxt, path.copy(), visited.copy())


# =====================
# POINT D'ENTRÉE
# =====================
vprint("Démarrage de la détection TTCA")

for pid, p in principals.items():
    if p.get("controlled", False):
        vprint(f"Principal contrôlé détecté : {pid}")
        dfs(pid, pid, [], set())
