import random
from seating_plan import SeatingPlan, Table

# Define the HillClimbing class which tries to optimize the seating plan using hill climbing
class HillClimbing:
    def __init__(self, seating_plan, max_iterations=10000):
        # Initialize with a given seating plan
        self.current_plan = seating_plan
        self.best_plan = seating_plan
        # Score the initial plan
        self.current_score = seating_plan.score()
        self.best_score = self.current_score
        # Set a limit for how many iterations the algorithm will run
        self.max_iterations = max_iterations

    # The main optimization loop
    def run(self):
        for _ in range(self.max_iterations):
            # Generate a "neighbor" plan by making a small change (swapping guests)
            new_plan = self._generate_neighbor()
            new_score = new_plan.score()

            # If the new plan is better, move to it
            if new_score > self.current_score:
                self.current_plan = new_plan
                self.current_score = new_score

                # If it's the best so far, update the best plan
                if new_score > self.best_score:
                    self.best_plan = new_plan
                    self.best_score = new_score

        # Return the best plan found and its score
        return self.best_plan, self.best_score

    def _generate_neighbor(self):
        """
        Generates a neighboring solution by swapping two guests between two different tables.
        This is the "small step" used by hill climbing to explore new possibilities.
        """
        # Create a deep copy of the current seating plan
        new_plan = SeatingPlan(
            self.current_plan.guest_list,
            len(self.current_plan.tables),
            self.current_plan.tables[0].capacity
        )

        # Recreate tables and copy the guest assignments from the current plan
        new_plan.tables = [Table(table.capacity) for table in self.current_plan.tables]
        for i, table in enumerate(self.current_plan.tables):
            # Copy guest lists (shallow copy of guest references)
            new_plan.tables[i].guests = table.guests[:]

        # Randomly pick two different tables and swap a guest between them
        table1, table2 = random.sample(range(len(new_plan.tables)), 2)
        new_plan.swap_guests(table1, table2)

        return new_plan