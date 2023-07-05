import subprocess
import itertools
import tempfile
import os
import numpy as np

def run_verifyta(model_file, query_file):
    verifyta_path = r"C:\uppaal64-4.1.26-2\bin-Windows\verifyta.exe"
    command = [verifyta_path, model_file, query_file]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            print("An error occurred during verification.")
            print("\nError message:")
            print(result.stderr)
            return None
    except FileNotFoundError:
        print(f"Verifyta executable not found at {verifyta_path}. Please check the path.")
        return None

def generate_fault_states(faults):
    fault_states = []
    for i in range(1, len(faults) + 1):
        for combo in itertools.combinations(faults, i):
            fault_states.append("-".join(combo))
    return fault_states

def analyze_results(results, fault_states, queries):
    fault_results = []
    for i, result in enumerate(results):
        if "Formula is satisfied." in result:
            fault_results.append(fault_states[i])

    return fault_results

def minimize_fault_results(fault_results):
    min_fault_results = fault_results.copy()

    for fault_state in fault_results:
        fault_set = set(fault_state.split('-'))

        for other_fault_state in fault_results:
            if fault_state == other_fault_state:
                continue

            other_fault_set = set(other_fault_state.split('-'))

            if fault_set.issubset(other_fault_set):
                if other_fault_state in min_fault_results:
                    min_fault_results.remove(other_fault_state)

    return min_fault_results

if __name__ == "__main__":
    model_file = r"C:\Users\Chwarzenegger\Desktop\System Diagnosis\zhe\result\out.xml"
    query_file = r"C:\Users\Chwarzenegger\Desktop\System Diagnosis\Test\Query\queries-v2.q"
    
    faults = ["f1_breaker1_open", "f2_breaker1_lock", "f3_sensor2_reject", "f4_breaker2_open","f5_breaker2_lock","f6_sensor1_reject"]
    fault_states = generate_fault_states(faults)
    
    queries = []
    with open(query_file, "r") as f:
        queries = f.readlines()
    print(queries)

    results = []

    for i, query in enumerate(queries):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".q") as temp_query_file:
            temp_query_file.write(query)
            temp_query_file_path = temp_query_file.name
        
        print(f"Running query {i + 1}: {query.strip()}")

        result = run_verifyta(model_file, temp_query_file_path)
        if i == 0:
            if "Formula is satisfied" in result:
                print("No fault_results found.")
                continue
            else:
                continue
        results.append(result)

        os.remove(temp_query_file_path)


    # first_query_result = run_verifyta(model_file, query_file, queries[0])
    # if "Formula is satisfied." in first_query_result:
    #     print("No fault_results found.")
    # else:
    # for query in queries[1:]:
    #     print("1")
    #     result = run_verifyta(model_file, query_file, query)
    #     # if result is not None:
    #     results.append(result)
        # else:
        #     break


    fault_results = analyze_results(results, fault_states, queries)
    print("\nResults found:")
    for fault_result in fault_results:
        print(fault_result)


    min_fault_results = minimize_fault_results(fault_results)
    print("\nMinimal results found:")
    for fault_result in min_fault_results:
        print(fault_result)