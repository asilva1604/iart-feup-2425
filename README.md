# Wedding Seat Planner

This project is a seating plan optimizer for events like weddings. It uses various algorithms to optimize guest seating arrangements based on their preferences.

## Features

- Supports multiple optimization algorithms:
  - Simulated Annealing
  - Hill Climbing
  - Greedy
  - Tabu Search
  - Genetic Algorithm
  - K-Clustering
- Graphical User Interface (GUI) for easy interaction.
- Visual representation of seating plans.
- Comparison of algorithm performance.

---

## Requirements

- Python 3.13 or higher
- Required Python libraries:
  - `tkinter` (for GUI)
  - `matplotlib` (for visualizations)
  - `csv` (for input/output handling)
  - `numpy` (for numerical operations)
  - `pandas` (for data manipulation)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/asilva1604/iart-feup-2425
   cd iart-feup-2425
   ```

2. Install required Python libraries using `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   This will automatically install all the necessary dependencies for the project.

---

## How to Run

1. Navigate to the project directory:

   ```bash
   cd iart-feup-2425
   ```

2. Run the program:

   ```bash
   python3 src/main.py
   ```

---

## How to Use

1. **Select a Dataset**:

   - Use the dataset selection buttons to load a predefined dataset (e.g., `Small`, `Medium`, `Large`, `Extra Large`).

2. **Set Number of Tables**:

   - Enter the number of tables in the input field.

3. **Choose an Algorithm**:

   - Select an algorithm from the list of available options:
     - Simulated Annealing
     - Hill Climbing
     - Greedy
     - Tabu Search
     - Genetic Algorithm
     - K-Clustering

4. **Run the Program**:

   - Choose a run mode:
     - `Run All Algorithms`: Runs all algorithms and compares their results.
     - `Run Selected Algorithm`: Runs only the selected algorithm.
   - Click the `Run` button to start the optimization.

5. **View Results**:

   - The results panel displays the best score, execution time, and algorithm used.
   - The seating plan is visualized on the canvas.

6. **Stop the Program**:
   - Click the `X` button to close the application.

---

## Input Format

The input dataset must be a CSV file with the following columns:

- `Guest`: Name of the guest.
- `Preference_Guest`: Name of the guest they have a preference for.
- `Preference_Score`: Numeric score indicating the strength of the preference.

Example:

```csv
Guest,Preference_Guest,Preference_Score
Alice,Bob,10
Alice,Charlie,5
Bob,Alice,8
Charlie,Alice,6
```

---

## Output

- The program outputs the optimized seating plan and its score.
- Results can be saved to a CSV file using the `write_output_csv` function in `utils.py`.

---

## Troubleshooting

- **Overlapping Chairs**: Ensure the number of tables is appropriate for the dataset size.

---

## License

This project is licensed under the FEUP License. See the `LICENSE` file for details.

---

## Authors

- Alexandre Silva => up2022...
- Bruno Forteiro => up202209730
- Beatriz Remondes => up2022...
