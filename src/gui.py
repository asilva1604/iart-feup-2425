import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from algorithms import SimulatedAnnealing, HillClimbing, Greedy, TabuSearch
from seating_plan import SeatingPlan
from utils import read_input_csv

class SeatingPlanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Seating Plan Optimizer")
        self.root.geometry("600x400")

        # Input file selection
        self.input_file_label = tk.Label(root, text="Input File:")
        self.input_file_label.pack(pady=5)
        self.input_file_entry = tk.Entry(root, width=50)
        self.input_file_entry.pack(pady=5)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Algorithm selection
        self.algorithm_label = tk.Label(root, text="Select Algorithm:")
        self.algorithm_label.pack(pady=5)
        self.algorithm_combobox = ttk.Combobox(root, values=["Simulated Annealing", "Hill Climbing", "Greedy", "Tabu Search"])
        self.algorithm_combobox.pack(pady=5)

        # Run button
        self.run_button = tk.Button(root, text="Run", command=self.run_algorithm)
        self.run_button.pack(pady=10)

        # Results display
        self.results_text = tk.Text(root, height=15, width=70)
        self.results_text.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, file_path)

    def run_algorithm(self):
        input_file = self.input_file_entry.get()
        algorithm = self.algorithm_combobox.get()

        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return

        if not algorithm:
            messagebox.showerror("Error", "Please select an algorithm.")
            return

        try:
            # Read input data
            guests = read_input_csv(input_file)
            table_capacity = 3
            num_tables = (len(guests) + table_capacity - 1) // table_capacity
            seating_plan = SeatingPlan(guests, num_tables=num_tables, table_capacity=table_capacity)

            # Run the selected algorithm
            if algorithm == "Simulated Annealing":
                optimizer = SimulatedAnnealing(seating_plan)
                best_plan, best_score = optimizer.run()
            elif algorithm == "Hill Climbing":
                optimizer = HillClimbing(seating_plan)
                best_plan, best_score = optimizer.run()
            elif algorithm == "Greedy":
                optimizer = Greedy(guests, num_tables=num_tables, table_capacity=table_capacity)
                best_plan = optimizer.run()
                # Calculate the total score for the Greedy algorithm
                best_score = sum(
                    guest.get_preference(other)
                    for table in best_plan
                    for guest in table.guests
                    for other in table.guests
                    if guest != other
                )
            elif algorithm == "Tabu Search":
                optimizer = TabuSearch(seating_plan)
                best_plan, best_score = optimizer.run()
            else:
                messagebox.showerror("Error", "Invalid algorithm selected.")
                return

            # Display results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Algorithm: {algorithm}\n")
            self.results_text.insert(tk.END, f"Best Score: {best_score}\n")
            self.results_text.insert(tk.END, f"Seating Plan:\n{best_plan}\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingPlanGUI(root)
    root.mainloop()