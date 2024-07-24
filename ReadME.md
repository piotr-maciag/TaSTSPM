
readme_content = """
# TaSTSPM: Temporal and Spatial-Temporal Sequential Pattern Mining

## Overview

TaSTSPM (Temporal and Spatial-Temporal Sequential Pattern Mining) is a Python implementation for discovering spatio-temporal sequential patterns in datasets where events are tagged with both spatial and temporal attributes. This implementation leverages efficient spatial indexing using R-tree for faster neighborhood calculations.

## Features

- **Spatio-temporal sequence mining**: Discover patterns based on both spatial and temporal proximity.
- **Efficient indexing**: Uses R-tree for efficient spatial querying.
- **Flexible distance calculations**: Supports both Earth (Haversine) and Euclidean distance calculations.
- **Verbose logging**: Provides detailed logging for understanding the execution process.

## Requirements

- Python 3.x
- `pandas`
- `rtree`
- `numpy`

## Installation

Install the required Python packages using pip:

\`\`\`bash
pip install pandas rtree numpy
\`\`\`

## Usage

### Dataset Preparation

Ensure your dataset is in CSV format with columns for `Instance_ID`, `Event_type`, `Location_X`, `Location_Y`, and `Occurrence_time`.

### Code Example

\`\`\`python
from src.Sequence import *

# Load dataset
dataset = Dataset("path/to/your/dataset.csv")

# Define parameters
F = ['A', 'B', 'C', 'D']  # Set of event types
R = 10  # Spatial neighborhood radius
T = 20  # Temporal neighborhood threshold
theta = 0.5  # PI threshold
stq = [Sequence(event_types=['A']), Sequence(event_types=['B'])]  # Spatio-temporal query

# Run TaSTSPM algorithm
TaSTSPs = tastsp_algorithm(dataset, F, R, T, theta, stq, distance_type='Earth', verbose=1)

# Output results
for sequence in TaSTSPs:
print(sequence)
\`\`\`

### Key Functions

- **Dataset Class**: Manages event data, spatial indexing, and time range calculations.
    - \`add_event(event)\`: Adds an event to the dataset.
    - \`load_data(file_path)\`: Loads data from a CSV file.
    - \`get_times(event_type)\`: Retrieves time range for a given event type.

- **Sequence Class**: Represents a sequence of events and manages spatio-temporal calculations.
    - \`calculate_I(index, D, R, T)\`: Calculates the neighborhood set I for the given index.
    - \`calculate_I_backward(index, D, R, T)\`: Calculates the backward neighborhood set I.
    - \`calculate_PI(PR_func, D, R, T)\`: Calculates the probability index PI for the sequence.
    - \`is_subsequence_of(other)\`: Checks if the sequence is a subsequence of another.
    - \`is_supersequence_of(other)\`: Checks if the sequence is a supersequence of another.

- **tastsp_algorithm()**: Main function to run the TaSTSPM algorithm.
    - \`tastsp_algorithm(D, F, R, T, theta, stq, distance_type='Earth', verbose=0)\`: Executes the algorithm with given parameters.

### Parameters

- **D**: Dataset object containing the event instances.
- **F**: Set of event types.
- **R**: Spatial neighborhood radius.
- **T**: Temporal neighborhood threshold.
- **theta**: PI threshold.
- **stq**: Spatio-temporal sequence query.
- **distance_type**: Type of distance calculation ('Earth' for Haversine or 'Euclidean').
- **verbose**: Verbosity level for logging.

## Contact

For any questions or issues, please contact [piotr.maciag@pw.edu.pl].