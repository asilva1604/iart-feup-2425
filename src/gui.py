import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from math import cos, sin, pi  # Import cos, sin, and pi for angle calculations
from algorithms import SimulatedAnnealing, HillClimbing, Greedy, TabuSearch
from seating_plan import SeatingPlan
from utils import read_input_csv

class SeatingPlanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Seating Plan Optimizer")
        self.root.geometry("1000x800")  # Increased canvas size

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

        # Canvas for visualizing tables
        self.canvas = tk.Canvas(root, width=950, height=600, bg="white")  # Larger canvas
        self.canvas.pack(pady=10)

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

            # Visualize the seating plan
            self.visualize_seating_plan(best_plan, best_score)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def visualize_seating_plan(self, seating_plan, total_score):
        self.canvas.delete("all")  # Clear the canvas

        # Display total score at the top of the canvas with padding
        self.canvas.create_text(475, 30, text=f"Total Score: {total_score}", font=("Arial", 14, "bold"))

        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate grid dimensions for table placement
        num_tables = len(seating_plan.tables)
        aspect_ratio = canvas_width / canvas_height
        grid_cols = int((num_tables * aspect_ratio) ** 0.5)  # Calculate columns based on aspect ratio
        grid_rows = (num_tables + grid_cols - 1) // grid_cols  # Calculate rows based on columns

        # Dynamically adjust table size and spacing
        max_table_radius = 50  # Maximum table radius
        min_table_radius = 10  # Minimum table radius
        table_radius = max(min_table_radius, min(max_table_radius, min(canvas_width // (grid_cols * 3), canvas_height // (grid_rows * 3))))
        spacing_x = canvas_width // grid_cols  # Horizontal spacing
        spacing_y = (canvas_height - 100) // grid_rows  # Vertical spacing (subtract padding for score text)

        # Adjust table radius to fit within spacing
        table_radius = min(table_radius, spacing_x // 3, spacing_y // 3)

        for i, table in enumerate(seating_plan.tables):
            # Calculate table position in grid
            col = i % grid_cols
            row = i // grid_cols
            table_x = spacing_x // 2 + col * spacing_x
            table_y = spacing_y // 2 + row * spacing_y + 50  # Add padding below the score text

            # Draw table (circle)
            self.canvas.create_oval(
                table_x - table_radius, table_y - table_radius,
                table_x + table_radius, table_y + table_radius,
                fill="lightblue"
            )

            # Draw guests around the table
            num_guests = len(table.guests)
            for j, guest in enumerate(table.guests):
                angle = 2 * pi * j / num_guests  # Use pi for angle calculation
                guest_x = table_x + table_radius * 0.8 * cos(angle)
                guest_y = table_y + table_radius * 0.8 * sin(angle)
                self.canvas.create_text(guest_x, guest_y, text=guest.name, font=("Arial", 8))

if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingPlanGUI(root)
    root.mainloop()