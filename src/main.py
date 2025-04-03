# from utils import read_input_csv, write_output_csv
# from __init__ import run_all_algorithms
import tkinter as tk
import gui


# def main():
#     # Read input CSV
#     input_file_path = './input.csv'
#     guests = read_input_csv(input_file_path)

#     # Calculate the number of tables required
#     table_capacity = 3
#     num_tables = (len(guests) + table_capacity - 1) // table_capacity  # Ceiling division

#     # Run all algorithms
#     results = run_all_algorithms(guests, num_tables, table_capacity)

#     # Write output CSV
#     output_file_path = 'output.csv'
#     write_output_csv(output_file_path, results)

#     # Print results
#     for result in results:
#         print(f"\n{result[0]} Optimized Seating Plan:\n", result[3])
#         print(f"Best Score: {result[1]}")

# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    root = tk.Tk()
    app = gui.SeatingPlanGUI(root)
    root.mainloop()

