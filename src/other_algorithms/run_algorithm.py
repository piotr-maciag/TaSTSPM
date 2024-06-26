import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.other_algorithms.load_data import Dataset
from src.other_algorithms.sequence_mining import CST_SPMiner, STBFM

def run_algorithm(dataset_path, R, T, theta, algorithm, verbose=0):
    dataset = Dataset(dataset_path)

    if algorithm == 'CST_SPMiner':
        result = CST_SPMiner(dataset, theta, T, R, verbose)
    elif algorithm == 'STBFM':
        result = STBFM(dataset, theta, T, R, verbose)
    else:
        raise ValueError("Unknown algorithm specified.")

    return result

def print_sequences(sequences_tree):
    for level, sequences in enumerate(sequences_tree):
        print(f"Level {level}:")
        for seq in sequences:
            print(seq)
        print()

if __name__ == "__main__":
    dataset_path = 'path/to/dataset.csv'
    R = 50.0
    T = 10.0
    theta = 0.1

    # Running CST_SPMiner
    result_CST_SPMiner = run_algorithm(dataset_path, R, T, theta, 'CST_SPMiner')
    print("CST_SPMiner Result:", result_CST_SPMiner)

    # Running STBFM
    result_STBFM = run_algorithm(dataset_path, R, T, theta, 'STBFM')
    print("STBFM Result:", result_STBFM)