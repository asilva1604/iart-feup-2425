import random
import time  # Import time for measuring execution time
from seating_plan import SeatingPlan, Table

# This class implements a K-Means-style clustering algorithm adapted for seating guests
class KClustering:
    def __init__(self, guests, num_tables, table_capacity, max_iterations=100):
        self.guests = guests
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.max_iterations = max_iterations

    def initialize_random_tables(self):
        """Randomly assign guests to tables to start the clustering process."""
        tables = [Table(self.table_capacity) for _ in range(self.num_tables)]
        shuffled_guests = self.guests[:]
        random.shuffle(shuffled_guests)

        # Assign each guest to a random table with available space
        for guest in shuffled_guests:
            available_tables = [table for table in tables if not table.is_full()]
            if available_tables:
                random.choice(available_tables).add_guest(guest)

        return tables

    def initialize_centroids(self):
        """Randomly select guests to act as initial centroids (representative of a table)."""
        return random.sample(self.guests, self.num_tables)

    def assign_guests_to_tables(self, centroids):
        """
        Assign each guest to the table whose centroid they prefer most,
        without exceeding table capacities.
        """
        tables = [Table(self.table_capacity) for _ in range(self.num_tables)]
        unassigned_guests = []

        for guest in self.guests:
            # Rank centroids by how much this guest prefers them
            preferences = [
                (idx, guest.get_preference(centroids[idx]))
                for idx in range(len(centroids))
            ]
            preferences.sort(key=lambda x: -x[1])  # Descending order

            # Try to assign the guest to their most preferred available table
            assigned = False
            for idx, _ in preferences:
                if not tables[idx].is_full():
                    tables[idx].add_guest(guest)
                    assigned = True
                    break

            # If all preferred tables are full, hold for later assignment
            if not assigned:
                unassigned_guests.append(guest)

        # Add remaining guests to any available table
        for guest in unassigned_guests:
            for table in tables:
                if not table.is_full():
                    table.add_guest(guest)
                    break

        return tables

    def calculate_new_centroids(self, tables):
        """
        For each table, select the guest who has the highest average preference
        for the others at that table to act as the new centroid.
        """
        centroids = []
        for table in tables:
            if not table.guests:
                # Handle empty table by assigning a random guest as the centroid
                centroids.append(random.choice(self.guests))
            else:
                # Find the guest who is most "liked" or compatible with the others
                centroids.append(
                    max(
                        table.guests,
                        key=lambda guest: sum(
                            guest.get_preference(other)
                            for other in table.guests if guest != other
                        )
                    )
                )
        return centroids

    def run(self):
        """Run the K-Clustering algorithm to generate an optimized seating plan."""
        start_time = time.time()  # Start measuring time

        # Step 1: Initialize tables and centroids
        tables = self.initialize_random_tables()
        centroids = self.calculate_new_centroids(tables)

        best_plan = None
        best_score = float('-inf')

        for _ in range(self.max_iterations):
            # Step 2: Assign guests to the most compatible tables (based on centroids)
            tables = self.assign_guests_to_tables(centroids)

            # Step 3: Create and score the current seating plan
            seating_plan = SeatingPlan(self.guests, self.num_tables, self.table_capacity)
            seating_plan.tables = tables
            score = seating_plan.score()

            # Step 4: Keep the best scoring plan
            if score > best_score:
                best_plan = seating_plan
                best_score = score

            # Step 5: Recalculate centroids based on the new table composition
            new_centroids = self.calculate_new_centroids(tables)

            # Step 6: Stop if centroids no longer change (convergence)
            if all(new_centroids[i].name == centroids[i].name for i in range(len(centroids))):
                break

            centroids = new_centroids

        end_time = time.time()  # Stop measuring time
        execution_time = end_time - start_time

        # Return the best seating plan, its score, and how long it took
        return best_plan, best_score, execution_time
