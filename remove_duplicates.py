import os


for filename in [f for f in os.listdir('.') if f[-3:] == 'csv']:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            if line not in lines:
                lines.append(line)
    with open(filename, 'w') as file:
        file.write(''.join(lines))
