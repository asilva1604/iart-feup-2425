from itertools import combinations
from seating_plan import SeatingPlan, Table

class BruteForce:
    def __init__(self, guests, num_tables, table_capacity):
        self.guests = guests
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.max_partitions = min(1000, 2 ** len(guests))  # Dynamically limit partitions

    def generate_table_partitions(self):
        """Generate ordered and valid partitions of guests into tables."""
        partitions = []
        count = [0]

        def generate_partitions_recursive(remaining_guests, current_tables, remaining_tables):
            if remaining_tables == 0:
                if not remaining_guests:
                    partitions.append(list(current_tables))
                    count[0] += 1
                return

            if count[0] >= self.max_partitions:
                return

            if not remaining_guests:
                return

            for i in range(1, min(len(remaining_guests) + 1, self.table_capacity + 1)):
                first_table = list(remaining_guests[:i])
                remaining = remaining_guests[i:]
                generate_partitions_recursive(remaining, current_tables + [first_table], remaining_tables - 1)

        generate_partitions_recursive(self.guests, [], self.num_tables)
        return partitions

    def run(self):
        """Run brute force to find the best seating arrangement."""
        if self.num_tables > len(self.guests):
            raise ValueError("Number of tables cannot exceed the number of guests.")

        best_plan = None
        best_score = float('-inf')

        partitions = self.generate_table_partitions()

        for partition in partitions:
            seating_plan = SeatingPlan(self.guests, self.num_tables, self.table_capacity)

            for table, guests in zip(seating_plan.tables, partition):
                table.guests = guests

            score = seating_plan.score()

            if score > best_score:
                best_score = score
                best_plan = seating_plan

        return best_plan, best_score