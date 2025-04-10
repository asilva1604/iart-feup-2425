import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from math import cos, sin, pi, ceil
from algorithms import SimulatedAnnealing, HillClimbing, Greedy, TabuSearch, GeneticAlgorithm, KClustering
import os
from seating_plan import SeatingPlan
from utils import read_input_csv
from __init__ import run_all_algorithms  
import time  

class SeatingPlanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Seating Plan Optimizer")
        self.root.geometry("2400x1200")  # Increased width to accommodate results panel
        self.root.configure(bg="#e9ecef")
        
        # Add title at the top
        self.title_label = tk.Label(root, text="Wedding Seat Planner", bg="#e9ecef", font=("Arial", 16, "bold"), fg="#343a40")
        self.title_label.pack(pady=(10, 20))  # Add padding at the top and bottom

        # Get the absolute path to the project directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Predefined datasets
        self.datasets = {
            "Small": os.path.join(BASE_DIR, "datasets", "small.csv"),
            "Medium": os.path.join(BASE_DIR, "datasets", "medium.csv"),
            "Large": os.path.join(BASE_DIR, "datasets", "large.csv"),
            "Extra Large": os.path.join(BASE_DIR, "datasets", "extra_large.csv")
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
        
        # Algorithm selection buttons
        self.algorithm_label = tk.Label(root, text="Select Algorithm:", bg="#e9ecef", font=("Arial", 12, "bold"), fg="#343a40")
        self.algorithm_label.pack(pady=5)
        self.algorithm_frame = tk.Frame(root, bg="#e9ecef")
        self.algorithm_frame.pack(pady=5)

        self.selected_algorithm = None
        self.algorithm_buttons = {}
        algorithms = ["Simulated Annealing", "Hill Climbing", "Greedy", "Tabu Search", "Genetic Algorithm", "k-clustering"]
        for algorithm in algorithms:
            btn = tk.Button(self.algorithm_frame, text=algorithm, command=lambda alg=algorithm: self.select_algorithm(alg),
                            bg="#f8f9fa", fg="#343a40", font=("Arial", 10), relief=tk.RAISED, borderwidth=2)
            btn.pack(side=tk.LEFT, padx=5)
            self.algorithm_buttons[algorithm] = btn

        # Run mode selection buttons
        self.run_mode_label = tk.Label(root, text="Run Mode:", bg="#e9ecef", font=("Arial", 12, "bold"), fg="#343a40")
        self.run_mode_label.pack(pady=5)
        self.run_mode_frame = tk.Frame(root, bg="#e9ecef")
        self.run_mode_frame.pack(pady=5)

        self.selected_run_mode = None
        self.run_mode_buttons = {}
        run_modes = ["Run All Algorithms", "Run Selected Algorithm"]
        for mode in run_modes:
            btn = tk.Button(self.run_mode_frame, text=mode, command=lambda m=mode: self.select_run_mode(m),
                            bg="#f8f9fa", fg="#343a40", font=("Arial", 10), relief=tk.RAISED, borderwidth=2)
            btn.pack(side=tk.LEFT, padx=5)
            self.run_mode_buttons[mode] = btn
        
        # Run button
        self.run_button = tk.Button(root, text="Run", command=self.run_algorithm, bg="#ff7f50", fg="black", font=("Arial", 12, "bold"))
        self.run_button.pack(pady=10)
        
        # Stop button
        self.stop_button = tk.Button(root, text="X", command=self.stop_app, bg="#dc3545", fg="white", font=("Arial", 12, "bold"), borderwidth=0, highlightthickness=0)
        self.stop_button.pack(pady=10)
        self.stop_button.place(x=0, y=0)

        # Frame for canvas and scrollbars
        self.canvas_frame = tk.Frame(root, bg="#e9ecef")
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for visualization with scrollbars
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 2400, 2400))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure canvas to work with scrollbars
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        self.selected_file = None  # Variable to store selected dataset

        # Results panel
        self.results_frame = tk.Frame(root, bg="#f8f9fa", width=1200, height=400, relief=tk.RIDGE, borderwidth=2)
        self.results_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.results_label = tk.Label(self.results_frame, text="Algorithm Results", bg="#f8f9fa", font=("Arial", 12, "bold"), fg="#343a40")
        self.results_label.pack(pady=5)
        self.results_text = tk.Text(self.results_frame, wrap=tk.WORD, font=("Arial", 10), bg="#ffffff", fg="#343a40", state=tk.DISABLED, width=30, height=35)
        self.results_text.pack(pady=5, padx=5)

        # Checkbox for enabling file output
        self.file_output_enabled = tk.BooleanVar(value=False)
        self.file_output_checkbox = tk.Checkbutton(
            root, text="Enable File Output", variable=self.file_output_enabled,
            bg="#e9ecef", font=("Arial", 10), fg="#343a40", selectcolor="#ffffff"
        )
        self.file_output_checkbox.pack(pady=5)
    
    def select_algorithm(self, algorithm):
        """Highlight the selected algorithm button."""
        if self.selected_algorithm:
            self.algorithm_buttons[self.selected_algorithm].config(bg="#f8f9fa", relief=tk.RAISED)
        self.selected_algorithm = algorithm
        self.algorithm_buttons[algorithm].config(bg="#ffffff", relief=tk.SUNKEN)

    def select_run_mode(self, mode):
        """Highlight the selected run mode button."""
        if self.selected_run_mode:
            self.run_mode_buttons[self.selected_run_mode].config(bg="#0000FF", relief=tk.RAISED)
        self.selected_run_mode = mode
        self.run_mode_buttons[mode].config(bg="#ffffff", relief=tk.SUNKEN)
    
    def load_dataset(self, file_path):
        self.selected_file = file_path
        messagebox.showinfo("Dataset Selected", f"Loaded dataset: {os.path.basename(file_path)}")
    
    def run_algorithm(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a dataset.")
            return
        
        num_tables = self.num_tables_entry.get()
        
        if not num_tables.isdigit() or int(num_tables) <= 0:
            messagebox.showerror("Error", "Please enter a valid number of tables.")
            return
        
        num_tables = int(num_tables)
        
        try:
            guests = read_input_csv(self.selected_file)
            table_capacity = max(2, ceil(len(guests) / num_tables))
            
            # Check the selected run mode
            run_mode = self.selected_run_mode
            output_data = []  # To store results for file output
            # In the run_algorithm method, change these lines:
            if run_mode == "Run All Algorithms":
                results = []
                for algorithm in self.algorithm_buttons.keys():
                    best_plan, best_score, time_taken = self.run_selected_algorithm(algorithm, guests, num_tables, table_capacity)
                    results.append([algorithm, best_score, time_taken, best_plan])
                    output_data.append((algorithm, best_score, time_taken, best_plan))  # Now includes best_plan
                self.display_results(results)
                best_plan, best_score = results[0][3], results[0][1]
                self.visualize_seating_plan(best_plan, best_score)
            elif run_mode == "Run Selected Algorithm":
                algorithm = self.selected_algorithm
                if not algorithm:
                    messagebox.showerror("Error", "Please select an algorithm.")
                    return
                
                best_plan, best_score, time_taken = self.run_selected_algorithm(algorithm, guests, num_tables, table_capacity)
                self.visualize_seating_plan(best_plan, best_score)
                self.display_results([[algorithm, best_score, time_taken, best_plan]])
                output_data.append((algorithm, best_score, time_taken, best_plan))  # Now includes best_plan
            
            # Write results to file if file output is enabled
            if self.file_output_enabled.get():
                self.write_results_to_file(output_data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def write_results_to_file(self, results):
        """Writes the results to a file in the output folder, including table assignments."""
        import os

        # Get the base directory and create the output folder if it doesn't exist
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(BASE_DIR, "output")
        os.makedirs(output_dir, exist_ok=True)

        # Define the output file path
        output_file = os.path.join(output_dir, "results.txt")

        # Write results to the file
        with open(output_file, "w") as f:
            for result in results:
                algorithm, score, time_taken, best_plan = result
                f.write(f"Algorithm: {algorithm}\n")
                f.write(f"Quality Score: {score}\n")
                f.write(f"Time Taken: {time_taken:.2f} seconds\n")
                
                # Write table assignments
                f.write("\nTable Assignments:\n")
                for i, table in enumerate(best_plan.tables if hasattr(best_plan, 'tables') else best_plan):
                    f.write(f"Table {i+1} Guests: ")
                    guest_names = [guest.name for guest in table.guests]
                    f.write(", ".join(guest_names) + "\n")
                
                f.write("\n" + "="*50 + "\n\n")  # Add separator between different algorithm results
    
    def run_selected_algorithm(self, algorithm, guests, num_tables, table_capacity):
        """Run the selected algorithm and return the best plan, score, and execution time."""
        seating_plan = SeatingPlan(guests, num_tables=num_tables, table_capacity=table_capacity)
        start_time = time.time()  # Start timing
        if algorithm == "Simulated Annealing":
            optimizer = SimulatedAnnealing(seating_plan)
            result = optimizer.run()
        elif algorithm == "Hill Climbing":
            optimizer = HillClimbing(seating_plan)
            result = optimizer.run()
        elif algorithm == "Greedy":
            optimizer = Greedy(guests, num_tables=num_tables, table_capacity=table_capacity)
            best_plan = optimizer.run()
            # Fix score calculation for Greedy
            best_score = sum(
                guest.get_preference(other)
                for table in best_plan
                for guest in table.guests
                for other in table.guests
                if guest != other
            )
            result = (best_plan, best_score)
        elif algorithm == "Tabu Search":
            optimizer = TabuSearch(seating_plan)
            result = optimizer.run()
        elif algorithm == "k-clustering":
            optimizer = KClustering(guests, num_tables=num_tables, table_capacity=table_capacity)
            result = optimizer.run()  # Already returns (best_plan, best_score, execution_time)
            return result  # Return directly for K-Clustering
        elif algorithm == "Genetic Algorithm":
            optimizer = GeneticAlgorithm(guests, num_tables=num_tables, table_capacity=table_capacity)
            result = optimizer.run()
        else:
            raise ValueError("Invalid algorithm selected.")
        end_time = time.time()  # End timing
        execution_time = end_time - start_time
        return result[0], result[1], execution_time  # Return plan, score, and time

    def display_results(self, results):
        """Display the results of all algorithms in the results panel."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)  # Clear previous results

        for result in results:
            algorithm, best_score, time_taken, _ = result
            self.results_text.insert(tk.END, f"Algorithm: {algorithm}\n")
            self.results_text.insert(tk.END, f"Best Score: {best_score}\n")
            self.results_text.insert(tk.END, f"Time Taken: {time_taken:.2f} seconds\n")
            self.results_text.insert(tk.END, "-" * 30 + "\n")

        self.results_text.config(state=tk.DISABLED)
    
    def stop_app(self):
        """Stops the application."""
        self.root.destroy()

    def visualize_seating_plan(self, seating_plan, total_score):
        self.canvas.delete("all")  # Clear the canvas

        # Display total score at the top of the canvas
        self.canvas.create_text(1200, 30, text=f"Total Score: {total_score}", font=("Arial", 14, "bold"), fill="#343a40")

        # Get canvas dimensions and adjust scroll region
        canvas_width = 2400
        canvas_height = 2400
        self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))

        tables = seating_plan.tables if hasattr(seating_plan, 'tables') else seating_plan

        # Calculate grid dimensions for table placement
        num_tables = len(tables)
        aspect_ratio = canvas_width / canvas_height
        grid_cols = int((num_tables * aspect_ratio) ** 0.5)
        grid_rows = (num_tables + grid_cols - 1) // grid_cols

        # Adjust table radius and spacing
        table_radius = min(50, min(canvas_width // (grid_cols * 4), canvas_height // (grid_rows * 4)))
        spacing_x = canvas_width // grid_cols
        spacing_y = canvas_height // grid_rows

        for i, table in enumerate(tables):
            col, row = i % grid_cols, i // grid_cols
            table_x = spacing_x // 2 + col * spacing_x
            table_y = spacing_y // 2 + row * spacing_y

            # Draw table (circle)
            self.canvas.create_oval(
                table_x - table_radius, table_y - table_radius,
                table_x + table_radius, table_y + table_radius,
                fill="#FF6347", outline="black", width=2
            )
            self.canvas.create_text(table_x, table_y, text=f"Table {i+1}", font=("Arial", 10, "bold"), fill="white")

            # Adjust seat placement radius to avoid overlapping
            seat_radius = table_radius + 30
            for j, guest in enumerate(table.guests):
                angle = 2 * pi * j / len(table.guests)
                guest_x = table_x + seat_radius * cos(angle)
                guest_y = table_y + seat_radius * sin(angle)
                guest_number = ''.join(filter(str.isdigit, guest.name))
                self.canvas.create_oval(
                    guest_x - 15, guest_y - 15,
                    guest_x + 15, guest_y + 15,
                    fill="#87CEEB", outline="black"
                )
                self.canvas.create_text(guest_x, guest_y, text=guest_number, font=("Arial", 8, "bold"), fill="black")

