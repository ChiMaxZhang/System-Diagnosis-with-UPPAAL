import itertools

def generate_fault_states(faults):
    fault_states = []
    for i in range(1, len(faults) + 1):
        for combo in itertools.combinations(faults, i):
            fault_states.append("".join(combo))
            # fault_states.append("-".join(combo))
    return fault_states

def generate_queries(faults, output_file):
    fault_states = generate_fault_states(faults)

    with open(output_file, 'w') as f:
        f.write("E<> obs.EndOfObs and faultsModel.NORMAL\n")
        for fault_state in fault_states:
            query = f"E<> obs.EndOfObs and faultsModel.{fault_state}\n"
            f.write(query)
    print("Successfully generate queries.q!")

if __name__ == "__main__":
    faults = ["F1_BREAKER1_OPEN", "F2_BREAKER1_LOCK", "F3_SENSOR2_REJECT", "F4_BREAKER2_OPEN","F5_BREAKER2_LOCK","F6_SENSOR1_REJECT"]
    output_file = r"C:\Users\Chwarzenegger\Desktop\System Diagnosis\Test\Query\queries-v2.q"

    generate_queries(faults, output_file)