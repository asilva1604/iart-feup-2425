import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from math import cos, sin, pi, ceil
from algorithms import SimulatedAnnealing, HillClimbing, Greedy, TabuSearch, GeneticAlgorithm, BruteForce
import os
from seating_plan import SeatingPlan
from utils import read_input_csv

class SeatingPlanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Seating Plan Optimizer")
        self.root.geometry("1000x800")
        self.root.configure(bg="#e9ecef")
        
        # Add title at the top
        self.title_label = tk.Label(root, text="Wedding Seat Planner", bg="#e9ecef", font=("Arial", 16, "bold"), fg="#343a40")
        self.title_label.pack(pady=(10, 20))  # Add padding at the top and bottom

        # Get the absolute path to the current script's directory
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # Predefined datasets
        self.datasets = {
            "Small": os.path.join(BASE_DIR, "small.csv"),
            "Medium": os.path.join(BASE_DIR, "medium.csv"),
            "Large": os.path.join(BASE_DIR, "large.csv"),
            "Extra Large": os.path.join(BASE_DIR, "extra_large.csv")
        }
        
        # Dataset selection buttons
        self.dataset_label = tk.Label(root, text="Select Dataset:", bg="#e9ecef", font=("Arial", 12, "bold"), fg="#343a40")
        self.dataset_label.pack(pady=5)
        
        self.dataset_frame = tk.Frame(root, bg="#e9ecef")
        self.dataset_frame.pack(pady=5)
        
        for dataset_name, dataset_path in self.datasets.items():
            btn = tk.Button(self.dataset_frame, text=dataset_name, command=lambda path=dataset_path: self.load_dataset(path),
                            bg="#0056b3", fg="white", font=("Arial", 10, "bold"))
            btn.pack(side=tk.LEFT, padx=5)
        
        # Number of tables selection
        self.num_tables_label = tk.Label(root, text="Number of Tables:", bg="#e9ecef", font=("Arial", 12, "bold"), fg="#343a40")
        self.num_tables_label.pack(pady=5)
        self.num_tables_entry = tk.Entry(root, width=10, font=("Arial", 10))
        self.num_tables_entry.pack(pady=5)
        
        # Algorithm selection
        self.algorithm_label = tk.Label(root, text="Select Algorithm:", bg="#e9ecef", font=("Arial", 12, "bold"), fg="#343a40")
        self.algorithm_label.pack(pady=5)
        self.algorithm_combobox = ttk.Combobox(root, values=["Simulated Annealing", "Hill Climbing", "Greedy", "Tabu Search", "Genetic Algorithm", "BruteForce"], font=("Arial", 10))
        self.algorithm_combobox.pack(pady=5)
        
        # Run button
        self.run_button = tk.Button(root, text="Run", command=self.run_algorithm, bg="#ff7f50", fg="black", font=("Arial", 12, "bold"))
        self.run_button.pack(pady=10)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(root, width=950, height=600, bg="white")
        self.canvas.pack(pady=10)
        
        self.selected_file = None  # Variable to store selected dataset
    
    def load_dataset(self, file_path):
        self.selected_file = file_path
        messagebox.showinfo("Dataset Selected", f"Loaded dataset: {os.path.basename(file_path)}")
    
    def run_algorithm(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a dataset.")
            return
        
        algorithm = self.algorithm_combobox.get()
        num_tables = self.num_tables_entry.get()
        
        if not num_tables.isdigit() or int(num_tables) <= 0:
            messagebox.showerror("Error", "Please enter a valid number of tables.")
            return
        
        num_tables = int(num_tables)
        
        try:
            guests = read_input_csv(self.selected_file)
            table_capacity = max(2, ceil(len(guests) / num_tables))
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
            elif algorithm == "BruteForce":
                optimizer = BruteForce(guests, num_tables=num_tables, table_capacity=table_capacity)
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
        self.canvas.create_text(475, 30, text=f"Total Score: {total_score}", font=("Arial", 14, "bold"), fill="#343a40")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        tables = seating_plan.tables if hasattr(seating_plan, 'tables') else seating_plan
        
        num_tables = len(tables)
        aspect_ratio = canvas_width / canvas_height
        grid_cols = int((num_tables * aspect_ratio) ** 0.5)
        grid_rows = (num_tables + grid_cols - 1) // grid_cols
        
        # Adjust table radius and spacing
        table_radius = min(50, min(canvas_width // (grid_cols * 4), canvas_height // (grid_rows * 4)))
        spacing_x = canvas_width // grid_cols
        spacing_y = (canvas_height - 100 - table_radius * 2.5) // grid_rows  # Account for table and seat radius
        
        for i, table in enumerate(tables):
            col, row = i % grid_cols, i // grid_cols
            table_x, table_y = spacing_x // 2 + col * spacing_x, spacing_y // 2 + row * spacing_y + 50
            self.canvas.create_oval(table_x - table_radius, table_y - table_radius, table_x + table_radius, table_y + table_radius, fill="#FF6347", outline="black", width=2)
            self.canvas.create_text(table_x, table_y, text=f"Table {i+1}", font=("Arial", 10, "bold"), fill="white")
            
            # Adjust seat placement radius to avoid overlapping
            seat_radius = table_radius * 1.8  # Increase distance between table and seats
            for j, guest in enumerate(table.guests):
                angle = 2 * pi * j / len(table.guests)
                guest_x, guest_y = table_x + seat_radius * cos(angle), table_y + seat_radius * sin(angle)
                guest_number = ''.join(filter(str.isdigit, guest.name))  # Extract the numeric part of the guest's name
                self.canvas.create_oval(guest_x - 10, guest_y - 10, guest_x + 10, guest_y + 10, fill="#87CEEB", outline="black")
                self.canvas.create_text(guest_x, guest_y, text=guest_number, font=("Arial", 8, "bold"), fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingPlanGUI(root)
    root.mainloop()
