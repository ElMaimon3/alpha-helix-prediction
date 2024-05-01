import numpy as np

def load_weights(filename):
    '''Loads the weights to be used in Naive Bayes, as well as the window size into a dictionary
    Inputs: filename (string)
    Returns: weights(dictionary)'''
    weights = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            weights[key] = float(value)
    return weights

weights = load_weights('parameters.txt')
window_size = int(weights['windowSize'])

with open('../input_file/infile.txt', 'r') as infile:
    with open('../output_file/outfile.txt','w') as outfile:
        lines = infile.readlines()  # Read all lines from the file
        # Iterate over the lines, processing two at a time
        for i in range(0, len(lines), 2):
            name_line = lines[i].strip()
            sequence_line = lines[i + 1].strip()
            helix_line = '' # Prediction will be stored here

            # Iterate over the sequence with windows of size window_size
            for j in range(len(sequence_line)):
                window = []
                if j < window_size // 2:# Beginning of the sequence
                    window.extend(['-'] * (window_size // 2 - j))
                    window.extend(sequence_line[:j + window_size // 2 + 1])
                elif j > len(sequence_line) - 1 - (window_size // 2):# End of the sequence
                    window.extend(sequence_line[j - window_size // 2:j + 1])
                    window.extend(sequence_line[j + 1:])
                    window.extend(['-'] * ((window_size // 2) - (len(sequence_line) - 1 - j)))
                else:# Middle of the sequence
                    window.extend(sequence_line[j - window_size // 2:j])
                    window.append(sequence_line[j])
                    window.extend(sequence_line[j + 1:j + window_size // 2 + 1])
                posterior_log_odds = weights['prior_log_odds']
                for a in window:# Predict using Naive Bayes
                    posterior_log_odds += weights[a]
                if posterior_log_odds > 0.1:
                    helix_line += 'H'
                else:
                    helix_line += '-'
            outfile.write(name_line+"\n"+sequence_line+"\n"+helix_line+"\n")


