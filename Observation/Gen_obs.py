import os
import xml.sax.saxutils

print(os.getcwd())  # Print current working directory

# Define the path to the folder you want to change to
folder_path = 'C:\\Users\\Chwarzenegger\\Desktop\\System Diagnosis\\Test\\Obs_v2'

# Change to the desired folder
os.chdir(folder_path)

# Now the current working directory (cwd) is changed to the desired folder
# You can perform operations in this folder or access files within this folder


def generate_uppaal_observations_template(input_file, output_file):
    with open(input_file, 'r') as f:
        # Read input file and extract data
        lines = f.readlines()
        transitions = [line.strip().split() for line in lines]

    # Generate UPPAAL XML template
    template = '<template>\n' \
               '    <name>Observation</name>\n' \
               '    <declaration>clock x;</declaration>\n'

    # Generate locations
    for i in range(len(transitions) + 1):
        template += f'    <location id="id{i+1}">\n'
        if i < len(transitions):
            template += f'        <name>state{i+1}</name>\n'
        else:
            template += f'        <name>end_of_obs</name>\n'
        template += '    </location>\n'

    # Generate initial location
    template += '    <init ref="id1" />\n'

    # Generate transitions
    for i, transition in enumerate(transitions):
        event, guard = transition
        guard_equation = f'x=={guard}'  # Translate guard into equation
        template += f'    <transition>\n'
        template += f'        <source ref="id{i+1}" />\n'
        template += f'        <target ref="id{i+2}" />\n'
        template += f'        <label kind="synchronisation">{xml.sax.saxutils.escape(event)}?</label>\n'
        template += f'        <label kind="guard">{xml.sax.saxutils.escape(guard_equation)}</label>\n'
        template += f'    </transition>\n'

    template += '</template>'

    with open(output_file, 'w') as f:
        # Write generated template to output file
        f.write(template)

    print(f'Success! UPPAAL observations template generated and saved to {output_file}.')


# Example usage
generate_uppaal_observations_template('obs1.txt', 'obs1.xml')
