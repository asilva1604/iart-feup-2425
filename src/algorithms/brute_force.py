from itertools import permutations
from seating_plan import SeatingPlan, Table

class BruteForce:
    def __init__(self, guests, num_tables, table_capacity):
        self.guests = guests
        self.num_tables = num_tables
        self.table_capacity = table_capacity

    def run(self):
        best_plan = None
        best_score = float('-inf')

        # Generate all possible permutations of guests
        for perm in permutations(self.guests):
            tables = [Table(self.table_capacity) for _ in range(self.num_tables)]
            table_idx = 0

            # Assign guests to tables based on the current permutation
            for guest in perm:
                while not tables[table_idx].add_guest(guest):
                    table_idx = (table_idx + 1) % self.num_tables

            # Create a seating plan and calculate its score
            seating_plan = SeatingPlan(self.guests, self.num_tables, self.table_capacity)
            seating_plan.tables = tables
            score = seating_plan.score()

            # Update the best plan if the current one is better
            if score > best_score:
                best_plan = seating_plan
                best_score = score

        return best_plan, best_score