import numpy as np


def store_dictionary_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        for key, value in dictionary.items():
            file.write(f"{key}:{value}\n")


def count(aa,helix):
    '''aa(char): the amino acid
    helix(char): the character of the helix line'''
    if helix == 'H':
        counts[aa][1] += 1
    else:
        counts[aa][0] += 1


amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V','-']
counts = {aa: [0, 0] for aa in amino_acids}
weights = {}
num_helix = 0
num_non_helix = 0

while True:
    window_size = int(input('Window Size?'))
    if (window_size % 2 == 1) and (window_size > 1):
        break
    print("Window size must be odd and larger than 1!")

with open('../training_data/labels.txt','r') as infile:
    lines = infile.readlines()  # Read all lines from the file

    # Iterate over the lines, processing three at a time
    for i in range(0, len(lines), 3):
        name_line = lines[i].strip()
        sequence_line = lines[i + 1].strip()
        helix_line = lines[i + 2].strip()
        for j in range(0,len(sequence_line)):
            window = []
            if j<window_size//2:
                for k in range((window_size//2)-j):
                    window.append('-')
                for k in range(j):
                    window.append(sequence_line[k])
                window.append(sequence_line[j])
                for k in range(1,(window_size//2)+1):
                    window.append(sequence_line[j+k])
            elif j>len(sequence_line)-1-(window_size//2):
                for k in range(1,(window_size//2)+1):
                    window.append(sequence_line[j-k])
                window.append(sequence_line[j])
                for k in range(j+1,len(sequence_line)):
                    window.append(sequence_line[k])
                for k in range((window_size//2)-len(sequence_line)-1-j):
                    window.append('-')
            else:
                for k in range(1,(window_size//2)+1):
                    window.append(sequence_line[j-k])
                    window.append(sequence_line[j+k])
                window.append(sequence_line[j])
            for a in window:
                count(a,helix_line[j])
            if helix_line[j] == 'H':
                num_helix += 1
            else:
                num_non_helix += 1

for key in counts:
    weights[key] = np.log((counts[key][1]/num_helix)/(counts[key][0]/num_non_helix))

weights['prior_log_odds'] = np.log(num_helix/num_non_helix)
weights['windowSize'] = window_size
store_dictionary_to_file(weights,'parameters.txt')
