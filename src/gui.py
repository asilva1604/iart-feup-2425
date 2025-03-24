import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from math import cos, sin, pi
from algorithms import SimulatedAnnealing, HillClimbing, Greedy, TabuSearch, GeneticAlgorithm
from seating_plan import SeatingPlan
from utils import read_input_csv

class SeatingPlanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Seating Plan Optimizer")
        self.root.geometry("1000x800")
        self.root.configure(bg="#e9ecef")  # Light neutral background color

        # Input file selection
        self.input_file_label = tk.Label(root, text="Input File:", bg="#e9ecef", font=("Arial", 12, "bold"), fg="#343a40")  # Dark text
        self.input_file_label.pack(pady=5)
        self.input_file_entry = tk.Entry(root, width=50, font=("Arial", 10))
        self.input_file_entry.pack(pady=5)
        
        # Browse button 
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file, bg="#0056b3", fg="black", font=("Arial", 10, "bold"))
        self.browse_button.pack(pady=5)

        # Number of tables selection
        self.num_tables_label = tk.Label(root, text="Number of Tables:", bg="#e9ecef", font=("Arial", 12, "bold"), fg="#343a40")
        self.num_tables_label.pack(pady=5)
        self.num_tables_entry = tk.Entry(root, width=10, font=("Arial", 10))
        self.num_tables_entry.pack(pady=5)

        # Algorithm selection
        self.algorithm_label = tk.Label(root, text="Select Algorithm:", bg="#e9ecef", font=("Arial", 12, "bold"), fg="#343a40")
        self.algorithm_label.pack(pady=5)
        self.algorithm_combobox = ttk.Combobox(root, values=["Simulated Annealing", "Hill Climbing", "Greedy", "Tabu Search", "Genetic Algorithm"], font=("Arial", 10))
        self.algorithm_combobox.pack(pady=5)

        # Run button with bright orange color
        self.run_button = tk.Button(root, text="Run", command=self.run_algorithm, bg="#ff7f50", fg="black", font=("Arial", 12, "bold"))
        self.run_button.pack(pady=10)

        # Canvas for visualization
        self.canvas = tk.Canvas(root, width=950, height=600, bg="white")
        self.canvas.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, file_path)

    def run_algorithm(self):
        input_file = self.input_file_entry.get()
        algorithm = self.algorithm_combobox.get()
        num_tables = self.num_tables_entry.get()

        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return
        
        if not num_tables.isdigit() or int(num_tables) <= 0:
            messagebox.showerror("Error", "Please enter a valid number of tables.")
            return
        
        num_tables = int(num_tables)

        try:
            guests = read_input_csv(input_file)
            table_capacity = max(2, len(guests) // num_tables)  # Ensure at least 2 per table
            seating_plan = SeatingPlan(guests, num_tables=num_tables, table_capacity=table_capacity)

            if algorithm == "Simulated Annealing":
                optimizer = SimulatedAnnealing(seating_plan)
                best_plan, best_score = optimizer.run()
            elif algorithm == "Hill Climbing":
                optimizer = HillClimbing(seating_plan)
                best_plan, best_score = optimizer.run()
            elif algorithm == "Greedy":
                optimizer = Greedy(guests, num_tables=num_tables, table_capacity=table_capacity)
                best_plan = optimizer.run()
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
            elif algorithm == "Genetic Algorithm":
                optimizer = GeneticAlgorithm(guests, num_tables=num_tables, table_capacity=table_capacity)
                best_plan, best_score = optimizer.run()
            else:
                messagebox.showerror("Error", "Invalid algorithm selected.")
                return

            self.visualize_seating_plan(best_plan, best_score)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def visualize_seating_plan(self, seating_plan, total_score):
        self.canvas.delete("all")
        self.canvas.create_text(475, 30, text=f"Total Score: {total_score}", font=("Arial", 14, "bold"), fill="#343a40")  # Dark text for score
        
        tables = seating_plan.tables if isinstance(seating_plan, SeatingPlan) else seating_plan
        num_tables = len(tables)
        spacing = 150
        start_x, start_y = 100, 100

        for i, table in enumerate(tables):
            table_x = start_x + (i % 5) * spacing
            table_y = start_y + (i // 5) * spacing

            # Table circle with better contrast
            self.canvas.create_oval(
                table_x - 30, table_y - 30, table_x + 30, table_y + 30,
                fill="#FF6347", outline="black", width=2  # A tomato red for tables
            )
            self.canvas.create_text(table_x, table_y, text=f"Table {i+1}", font=("Arial", 10, "bold"), fill="white")
            
            num_guests = len(table.guests)
            for j, guest in enumerate(table.guests):
                angle = 2 * pi * j / num_guests
                guest_x = table_x + 50 * cos(angle)
                guest_y = table_y + 50 * sin(angle)

                # Guest circles with distinct color
                self.canvas.create_oval(
                    guest_x - 10, guest_y - 10, guest_x + 10, guest_y + 10,
                    fill="#87CEEB", outline="black"  # Light blue for guests
                )
                self.canvas.create_text(guest_x, guest_y, text=guest.name[:2], font=("Arial", 8, "bold"), fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingPlanGUI(root)
    root.mainloop()
