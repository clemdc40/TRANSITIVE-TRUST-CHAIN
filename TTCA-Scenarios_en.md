# Transitive Trust Chain Abuse (Scenarios)

## Scenario 1 (basic):

3 Principals.
2 Relations.

Principal3 HAS_CAPABILITY Capability_critical

Principal1 **CAN_ACT_AS** Principal2
Principal2 **CAN_ACT_AS** Principal3

The attacker initially controls **Principal1**.  
Via Principal2, they can act as **Principal3** which has a critical capability. The TTCA is confirmed.

## Scenario 2 (False positive):

3 Principals.
2 Relations.

Principal1 HAS_CAPABILITY Capability_critical
Principal3 HAS_CAPABILITY Capability_critical

Principal1 **CAN_ACT_AS** Principal2
Principal2 **CAN_ACT_AS** Principal3

The attacker initially controls **Principal1**.  
Via Principal2, they can act as **Principal3** which has a critical capability. Given that **Principal1** already has a critical capability, a TTCA is triggered only if the critical capability is reachable by transitivity.

## Scenario 3 (Edge case):

3 Principals.
2 Relations.

Principal3 HAS_CAPABILITY Capability_critical

Principal1 **CAN_ACT_AS** Principal2
Principal2 **CAN_ACT_AS** Principal3
Principal1 **CAN_ACT_AS** Principal3

The attacker initially controls **Principal1**.  
Via **Principal2**, they can act as **Principal3** which has a critical capability. **Principal1** can also access **Principal3** directly. A TTCA is triggered only by transitivity; since there is a possibility to not rely on transitivity, the TTCA is not valid.
