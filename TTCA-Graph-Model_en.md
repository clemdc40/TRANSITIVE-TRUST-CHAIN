# Transitive Trust Chain Abuse (Graph)

![alt text](Graph.png)


## 1. Principals

Privilege levels (base, intermediate, critical) are given as illustration and do not constitute a fixed typology of principals.

In this example, we find 3 principals:
- Principal 1: base rights
- Principal 2: intermediate rights
- Principal 3: critical rights

## 2. Actions

Each edge has an action: CAN_ACT_AS.

The CAN_ACT_AS edge represents a delegation or impersonation relationship allowing a source principal to act with the effective privileges of the target principal.

Given that principal 2 can perform the actions of principal 3, this means that an attacker controlling principal 1 can abuse this and become principal 3 via principal 2.

This situation constitutes a Transitive Trust Chain Abuse, because access to principal 3 is made possible only by the composition of legitimate trust relationships, without any direct link existing between principal 1 and principal 3.

## 3. Capability

A Capability represents a capability or a critical power in the IAM system.  
It does not correspond to a specific technical resource, but to a risk boundary from a security standpoint.

Examples of capabilities:
- Global administration
- Identity and Access Management (IAM)
- Access to sensitive secrets
- Disabling or tampering with logging mechanisms

Capabilities are used to qualify the potential impact of a trust path.  
An escalation is considered critical when an initially low-privileged principal can, by transitivity, reach a sensitive capability.

## 4. Additional relations

In addition to the **CAN_ACT_AS** relation, the model introduces the following relation:

- **HAS_CAPABILITY (Principal → Capability)**  
  This relation indicates that a principal directly possesses a given capability.

The detection of a Transitive Trust Chain Abuse relies on identifying a path linking a principal controlled by an attacker to a critical capability, via one or more CAN_ACT_AS relations.

------------------------------------------------------------

In the previous example, principal 3 possesses a critical capability.  
Thus, although no direct link exists between principal 1 and this capability, it becomes reachable by transitivity via principal 2.

This path constitutes a Transitive Trust Chain Abuse.

## TTCA detection rule

A Transitive Trust Chain Abuse is detected when there exists a path in the graph satisfying the following conditions:

1. The path starts with a **principal controlled by the attacker**.
2. The path contains **at least two consecutive CAN_ACT_AS relations** between distinct principals.
3. The path ends with a **HAS_CAPABILITY relation** to a **critical capability**.
4. No direct relation exists between the initial principal and the final capability.

Formally, a path of the form:

Principal₀  
→ CAN_ACT_AS → Principal₁  
→ CAN_ACT_AS → …  
→ CAN_ACT_AS → Principalₙ  
→ HAS_CAPABILITY → Capability_critical  

with **n ≥ 1**, constitutes a TTCA.

A path does not constitute a TTCA if the initial principal already directly possesses the critical capability, or if a direct and explicit relation exists between the initial principal and that capability.
