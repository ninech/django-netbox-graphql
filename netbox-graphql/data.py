from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

def initialize_circuits():

    circuit_type = CircuitType(
        id = '111',
        name = 'Type 1',
        slug = 'type1'
    )
    circuit_type.save()
