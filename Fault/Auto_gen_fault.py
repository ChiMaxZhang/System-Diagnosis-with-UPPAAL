import xml.etree.ElementTree as ET
import os
import itertools

print(os.getcwd())  # Print current working directory

# Define the path to the folder you want to change to
folder_path = 'C:\\Users\\Chwarzenegger\\Desktop\\System Diagnosis\\Test\\Fault'

# Change to the desired folder
os.chdir(folder_path)

# Now the current working directory (cwd) is changed to the desired folder
# You can perform operations in this folder or access files within this folder

# Read input events from a text file

def read_events_from_file(file_path):
    events = []
    with open(file_path, 'r') as file:
        for line in file:
            event = line.strip()
            if event:
                events.append(event)
    return events

def generate_fault_template(events):
    states = generate_states(events)
    transitions = generate_transitions(states, events)
    
    template = "<template>\n"
    template += "  <name>Fault</name>\n"
    
    # Generate locations
    for i, state in enumerate(states):
        template += f"  <location id='id{i+1}'>\n"
        template += f"    <name>{state}</name>\n"
        template += "  </location>\n"
    
    # Generate initial state
    template += f"  <init ref='id1' />\n"
    
    # Generate transitions
    for i, transition in enumerate(transitions):
        source = transition[0]
        target = transition[1]
        event = transition[2]
        template += f"  <transition>\n"
        template += f"    <source ref='id{states.index(source)+1}' />\n"
        template += f"    <target ref='id{states.index(target)+1}' />\n"
        template += f"    <label kind='synchronisation'>{event}?</label>\n"
        template += "  </transition>\n"
    
    template += "</template>"
    
    return template

def generate_states(events):
    states = ["nofault"]
    for i in range(1, len(events) + 1):
        combinations = itertools.combinations(events, i)
        for combination in combinations:
            state = "-".join(combination)
            states.append(state)
    return states

def generate_transitions(states, events):
    transitions = []
    for i in range(len(states)):
        for j in range(len(states)):
            source = states[i]
            target = states[j]
            source_events = set(source.split("-"))
            target_events = set(target.split("-"))
            
            if target != "nofault":
                # Condition 1: If source state is "nofault" and target state has only one event
                if source == "nofault" and len(target_events) == 1:
                    event = target_events.pop()
                    transitions.append((source, target, event))
                
                # Condition 2: If source state is a subset of target state and target state has one more event than source state
                elif source_events.issubset(target_events) and len(target_events) - len(source_events) == 1:
                    event = (target_events - source_events).pop()
                    transitions.append((source, target, event))
            
    return transitions


# Example usage
input_file_path = "fault2.txt"  # Replace with the actual input file path
output_file_path = "fault4.xml"  # Replace with the desired output file path
events = read_events_from_file(input_file_path)
fault_template = generate_fault_template(events)
with open(output_file_path, 'w') as file:
    file.write(fault_template)
print(f"Fault template has been generated and saved to '{output_file_path}'.")
