# Transitive Trust Chain Abuse (Scénarios)

## Scénario 1 (basique) : 

3 Principals.
2 Relations.

Principal3 HAS_CAPABILITY Capability_critique

Principal1 **CAN_ACT_AS** Principal2
Principal2 **CAN_ACT_AS** Principal3

L'attaquant controle initialement **Principal1**. 
Par l'intermédiaire du Principal2, il peut agir comme **Principal3** ayant une capability critique. le TTCA est confirmé.

## Scénario 2 (Faux positif) : 

3 Principals.
2 Relations.

Principal1 HAS_CAPABILITY Capability_critique
Principal3 HAS_CAPABILITY Capability_critique

Principal1 **CAN_ACT_AS** Principal2
Principal2 **CAN_ACT_AS** Principal3

L'attaquant controle initialement **Principal1**. 
Par l'intermédiaire du Principal2, il peut agir comme **Principal3** ayant une capability critique. Etant donné que **Principal1** à déjà une capability critique. Un TTCA est déclanché uniquement si la capability critique est atteignable par transitivité.

## Scénario 3 (Cas limite) : 

3 Principals.
2 Relations.

Principal3 HAS_CAPABILITY Capability_critique

Principal1 **CAN_ACT_AS** Principal2
Principal2 **CAN_ACT_AS** Principal3
Principal1 **CAN_ACT_AS** Principal3

L'attaquant controle initialement **Principal1**. 
Par l'intermédiaire du **Principal2**, il peut agir comme **Principal3** ayant une capability critique. **Principal1** peut également accéder directement à **principal3**. Le TTCA est déclanché uniquement par transitivité, étant donné qu'il y à la possibilité de ne pas passer par la transitivité, le TTCA n'est pas valide.
