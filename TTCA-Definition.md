# Transitive Trust Chain Abuse (TTCA)

## 1. Introduction

Les systèmes modernes de gestion des identités et des accès dans le cloud (Cloud Identity and Access Management – IAM) reposent sur des **principaux** (identités) et des **relations de confiance** permettant la délégation d’actions entre ces identités. Dans ces environnements, l’accès à des ressources sensibles n’est souvent pas obtenu directement, mais via une succession de délégations légitimes entre services, rôles, workloads ou identités fédérées.

La **Transitive Trust Chain Abuse (TTCA)** désigne une classe de risques de sécurité dans laquelle un attaquant exploite une **chaîne de relations de confiance implicites et transitives** afin d’atteindre des privilèges ou des ressources qui n’étaient pas censés être accessibles depuis l’identité initialement compromise.

Le problème central ne réside pas dans une erreur de configuration isolée ou une vulnérabilité logicielle, mais dans la **composition de relations de confiance individuellement valides**, dont l’assemblage crée un chemin d’escalade inattendu.

Ce document vise à :
- définir formellement la classe d’abus TTCA ;
- délimiter clairement son périmètre ;
- proposer un modèle conceptuel générique et indépendant d’un fournisseur cloud ;
- illustrer le mécanisme par un exemple abstrait.

---

## 2. Définition formelle

### 2.1 Modélisation générale

Un environnement IAM cloud est modélisé comme un **graphe orienté étiqueté** :

- **G = (V, E)**  
  - **V** : ensemble des nœuds représentant les principaux et, éventuellement, les ressources.
  - **E** : ensemble des arêtes représentant les relations de confiance et les attributions de privilèges.

### 2.2 Principaux et privilèges

Un **principal** est une entité capable d’agir dans le système :
- utilisateur humain,
- rôle,
- service,
- workload,
- identité fédérée ou automatisée.

Un **privilège** correspond à l’autorisation d’effectuer une action donnée sur une cible donnée, sous certaines conditions.

On note **EffPriv(p)** l’ensemble des privilèges effectifs du principal **p**, après prise en compte des politiques, héritages, contraintes et contextes.

### 2.3 Relations de confiance

Une **relation de confiance** est définie comme suit :

- **Trust(p → q)** : le principal **p** peut, sous certaines conditions, obtenir la capacité d’agir en tant que **q** (totalement ou partiellement).

Ces relations sont :
- directionnelles ;
- conditionnelles ;
- légitimes du point de vue du système.

### 2.4 Définition de TTCA

On parle de **Transitive Trust Chain Abuse (TTCA)** lorsqu’il existe une séquence de principaux :

**P = (p₀, p₁, …, pₖ)** avec **k ≥ 1**, telle que :

1. L’attaquant contrôle initialement le principal **p₀**.
2. Pour chaque **i ∈ [0, k−1]**, une relation de confiance valide permet de passer de **pᵢ** à **pᵢ₊₁**.
3. Le principal final **pₖ** possède des privilèges effectifs considérés comme **critiques**, alors que ces privilèges ne sont ni directement ni explicitement accessibles depuis **p₀**.

Autrement dit, TTCA correspond à une **escalade de privilèges obtenue par transitivité**, résultant de l’enchaînement de relations de confiance pourtant légitimes individuellement.

---

## 3. Périmètre et non-objectifs

### 3.1 Dans le périmètre

TTCA couvre les situations impliquant :
- des chaînes de confiance multi-étapes ;
- plusieurs types de principaux (utilisateurs, services, workloads, rôles) ;
- des escalades dues à la **composition** des relations de confiance ;
- des environnements cloud modernes, simulés ou réels.

L’objectif principal est l’**identification et la compréhension des chemins d’escalade**, et non leur exploitation offensive.

### 3.2 Hors périmètre (Non-Goals)

TTCA ne vise pas à :
- exploiter des vulnérabilités logicielles (RCE, injections, bugs mémoire) ;
- analyser des erreurs IAM isolées sans transitivité ;
- fournir des guides d’attaque ou des procédures exploitables ;
- remplacer les moteurs d’évaluation de politiques natifs des fournisseurs cloud.

---

## 4. Modèle conceptuel

### 4.1 Principals

Chaque principal est modélisé comme un nœud possédant des attributs tels que :
- type (humain, service, workload, rôle, fédéré) ;
- contexte (tenant, projet, compte, environnement) ;
- sensibilité (optionnelle).

### 4.2 Relations de confiance

Les relations de confiance sont représentées par des arêtes orientées entre principaux, annotées par :
- le mécanisme de délégation ;
- les contraintes applicables ;
- le contexte d’exécution.

### 4.3 Transitivité

La transitivité n’est pas nécessairement explicite dans le système.  
Elle **émerge** de l’enchaînement de plusieurs délégations successives :

**p₀ → p₁ → … → pₖ**

Un chemin est considéré comme pertinent s’il mène à une augmentation significative du niveau de privilège ou du risque.

### 4.4 Privilèges effectifs

Les privilèges effectifs d’un principal résultent de :
- ses permissions directes ;
- les privilèges hérités ;
- les contraintes contextuelles.

Pour l’analyse TTCA, ces privilèges peuvent être résumés sous forme de **capacités critiques** (ex. : gestion IAM, accès à des secrets, modification de journaux).

---

## 5. Exemple abstrait

Considérons trois principaux :

- **A** : une identité de workload à privilèges limités.
- **B** : une identité d’automatisation intermédiaire.
- **C** : une identité administrative à privilèges élevés.

Relations de confiance :
1. **A → B** : A peut déléguer certaines actions à B.
2. **B → C** : B peut, dans certains contextes, agir en tant que C.

Profils de privilèges :
- **EffPriv(A)** : opérations basiques.
- **EffPriv(B)** : opérations étendues mais non critiques.
- **EffPriv(C)** : privilèges de gestion sensibles.

Individuellement, chaque relation est justifiée.  
Cependant, la chaîne **A → B → C** permet à un attaquant contrôlant **A** d’atteindre indirectement les privilèges de **C**.

Ce scénario constitue une TTCA car :
- l’escalade repose sur une chaîne de confiance multi-étapes ;
- aucun lien direct n’existe entre **A** et **C** ;
- le risque provient de la **composition** des relations, et non d’une faille unique.

---

## Conclusion   

La Transitive Trust Chain Abuse met en évidence une surface d’attaque systémique des environnements cloud : **la confiance elle-même**.  
L’objectif des travaux suivants sera de proposer une méthode de cartographie et de détection automatique de ces chaînes, afin d’améliorer l’audit et la conception sécurisée des architectures IAM cloud.
