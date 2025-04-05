import random
from seating_plan import SeatingPlan, Table

class TabuSearch:
    def __init__(self, seating_plan, tabu_tenure=5, max_iterations=1000):
        """
        Initialize the Tabu Search algorithm.
        
        Parameters:
        - seating_plan: Initial SeatingPlan object.
        - tabu_tenure: Number of iterations a solution remains in the tabu list.
        - max_iterations: Maximum number of iterations to run the search.
        """
        self.current_plan = seating_plan  # Current solution
        self.best_plan = seating_plan     # Best solution found so far
        self.current_score = seating_plan.score()  # Score of current plan
        self.best_score = self.current_score       # Score of best plan

        self.tabu_list = []              # List to keep recently visited solutions (tabu)
        self.tabu_tenure = tabu_tenure   # Maximum size of the tabu list
        self.max_iterations = max_iterations  # Stop after this many iterations

    def run(self):
        """Main optimization loop for Tabu Search."""
        for _ in range(self.max_iterations):
            # Generate neighboring solutions
            neighborhood = self._generate_neighbors()

            best_neighbor = None
            best_neighbor_score = float('-inf')

            # Evaluate all neighbors and select the best non-tabu one
            for neighbor in neighborhood:
                if neighbor not in self.tabu_list:
                    neighbor_score = neighbor.score()
                    if neighbor_score > best_neighbor_score:
                        best_neighbor = neighbor
                        best_neighbor_score = neighbor_score

            # Move to the best non-tabu neighbor
            if best_neighbor:
                self.current_plan = best_neighbor
                self.current_score = best_neighbor_score

                # Update the best plan if this neighbor is better
                if self.current_score > self.best_score:
                    self.best_plan = self.current_plan
                    self.best_score = self.current_score

                # Add the current plan to the tabu list
                self.tabu_list.append(self.current_plan)

                # Maintain tabu tenure (FIFO queue)
                if len(self.tabu_list) > self.tabu_tenure:
                    self.tabu_list.pop(0)

        return self.best_plan, self.best_score

    def _generate_neighbors(self):
        """
        Generates neighboring solutions by swapping guests between tables.

        Returns:
        - A list of new SeatingPlan objects with slightly modified seating.
        """
        neighbors = []
        for _ in range(10):  # Create 10 different neighbors
            # Deep copy the current seating plan
            new_plan = SeatingPlan(self.current_plan.guest_list, len(self.current_plan.tables), self.current_plan.tables[0].capacity)
            new_plan.tables = [Table(table.capacity) for table in self.current_plan.tables]
            
            # Copy guests to the new plan
            for i, table in enumerate(self.current_plan.tables):
                new_plan.tables[i].guests = table.guests[:]  # Shallow copy guest list per table

            # Randomly select two tables and perform a guest swap
            table1, table2 = random.sample(range(len(new_plan.tables)), 2)
            new_plan.swap_guests(table1, table2)

            # Add modified plan to neighborhood
            neighbors.append(new_plan)

        return neighbors
