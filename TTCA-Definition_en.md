# Transitive Trust Chain Abuse (TTCA)

## 1. Introduction

Modern cloud Identity and Access Management (IAM) systems rely on **principals** (identities) and **trust relationships** that allow delegation of actions between these identities. In these environments, access to sensitive resources is often not obtained directly but via a succession of legitimate delegations between services, roles, workloads, or federated identities.

**Transitive Trust Chain Abuse (TTCA)** refers to a class of security risks in which an attacker exploits an **implicit and transitive chain of trust relationships** to reach privileges or resources that were not intended to be accessible from the initially compromised identity.

The core problem does not lie in an isolated misconfiguration or a software vulnerability, but in the **composition of individually valid trust relationships**, whose assembly creates an unexpected escalation path.

This document aims to:
- formally define the TTCA class of abuse;
- clearly delimit its scope;
- propose a generic, cloud-provider-independent conceptual model;
- illustrate the mechanism with an abstract example.

---

## 2. Formal definition

### 2.1 General modeling

A cloud IAM environment is modeled as a **labeled directed graph**:

- **G = (V, E)**  
  - **V**: set of nodes representing principals and, optionally, resources.
  - **E**: set of edges representing trust relationships and privilege assignments.

### 2.2 Principals and privileges

A **principal** is an entity capable of acting in the system:
- a human user,
- a role,
- a service,
- a workload,
- a federated or automated identity.

A **privilege** corresponds to the authorization to perform a given action on a given target, under certain conditions.

We denote **EffPriv(p)** as the set of effective privileges of principal **p**, after accounting for policies, inheritance, constraints, and contexts.

### 2.3 Trust relationships

A **trust relationship** is defined as follows:

- **Trust(p → q)**: principal **p** can, under certain conditions, obtain the ability to act as **q** (fully or partially).

These relationships are:
- directional;
- conditional;
- legitimate from the system’s perspective.

### 2.4 Definition of TTCA

We speak of **Transitive Trust Chain Abuse (TTCA)** when there exists a sequence of principals:

**P = (p₀, p₁, …, pₖ)** with **k ≥ 1**, such that:

1. The attacker initially controls principal **p₀**.
2. For each **i ∈ [0, k−1]**, a valid trust relationship allows moving from **pᵢ** to **pᵢ₊₁**.
3. The final principal **pₖ** possesses effective privileges considered **critical**, while these privileges are neither directly nor explicitly accessible from **p₀**.

In other words, TTCA corresponds to a **privilege escalation obtained by transitivity**, resulting from the chaining of trust relationships that are individually legitimate.

---

## 3. Scope and non-goals

### 3.1 In scope

TTCA covers situations involving:
- multi-step chains of trust;
- multiple types of principals (users, services, workloads, roles);
- escalations due to the **composition** of trust relationships;
- modern cloud environments, simulated or real.

The primary objective is the **identification and understanding of escalation paths**, not their offensive exploitation.

### 3.2 Out of scope (Non-Goals)

TTCA does not aim to:
- exploit software vulnerabilities (RCE, injections, memory bugs);
- analyze isolated IAM errors without transitivity;
- provide guides for attacks or actionable procedures;
- replace native cloud provider policy evaluation engines.

---

## 4. Conceptual model

### 4.1 Principals

Each principal is modeled as a node possessing attributes such as:
- type (human, service, workload, role, federated);
- context (tenant, project, account, environment);
- sensitivity (optional).

### 4.2 Trust relationships

Trust relationships are represented as directed edges between principals, annotated with:
- the delegation mechanism;
- applicable constraints;
- the execution context.

### 4.3 Transitivity

Transitivity is not necessarily explicit in the system.  
It **emerges** from the chaining of multiple successive delegations:

**p₀ → p₁ → … → pₖ**

A path is considered relevant if it leads to a significant increase in privilege level or risk.

### 4.4 Effective privileges

A principal’s effective privileges result from:
- its direct permissions;
- inherited privileges;
- contextual constraints.

For TTCA analysis, these privileges can be summarized as **critical capabilities** (e.g., IAM management, access to secrets, log modification).

---

## 5. Abstract example

Consider three principals:

- **A**: a workload identity with limited privileges.
- **B**: an intermediate automation identity.
- **C**: an administrative identity with high privileges.

Trust relationships:
1. **A → B**: A can delegate certain actions to B.
2. **B → C**: B can, in certain contexts, act as C.

Privilege profiles:
- **EffPriv(A)**: basic operations.
- **EffPriv(B)**: extended but non-critical operations.
- **EffPriv(C)**: sensitive management privileges.

Individually, each relationship is justified.  
However, the chain **A → B → C** allows an attacker controlling **A** to indirectly reach **C**'s privileges.

This scenario constitutes a TTCA because:
- the escalation relies on a multi-step chain of trust;
- there is no direct link between **A** and **C**;
- the risk stems from the **composition** of relationships, not from a single flaw.

---

## Conclusion

Transitive Trust Chain Abuse highlights a systemic attack surface in cloud environments: **trust itself**.  
The goal of subsequent work will be to propose a method for mapping and automatically detecting these chains, in order to improve auditing and secure design of cloud IAM architectures.
