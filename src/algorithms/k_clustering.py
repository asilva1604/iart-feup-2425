import random
import time  # Import time for measuring execution time
from seating_plan import SeatingPlan, Table

class KClustering:
    def __init__(self, guests, num_tables, table_capacity, max_iterations=100):
        self.guests = guests
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.max_iterations = max_iterations
        
    def initialize_random_tables(self):
        """Randomly assign guests to tables to initialize the clustering process."""
        tables = [Table(self.table_capacity) for _ in range(self.num_tables)]
        shuffled_guests = self.guests[:]
        random.shuffle(shuffled_guests)

        for guest in shuffled_guests:
            # Find a table that is not full
            available_tables = [table for table in tables if not table.is_full()]
            if available_tables:
                random.choice(available_tables).add_guest(guest)

        return tables

    def initialize_centroids(self):
        """Randomly initialize centroids (representative guests for each table)."""
        return random.sample(self.guests, self.num_tables)

    def assign_guests_to_tables(self, centroids):
        """Assign each guest to the closest centroid (table)."""
        tables = [Table(self.table_capacity) for _ in range(self.num_tables)]
        for guest in self.guests:
            # Find the centroid with the highest preference score for this guest
            closest_centroid_idx = max(
                range(len(centroids)),
                key=lambda idx: guest.get_preference(centroids[idx])
            )
            tables[closest_centroid_idx].add_guest(guest)
        return tables

    def calculate_new_centroids(self, tables):
        """Calculate new centroids as the guest with the highest average preference in each table."""
        centroids = []
        for table in tables:
            if not table.guests:
                centroids.append(random.choice(self.guests))  # Handle empty tables
            else:
                centroids.append(
                    max(
                        table.guests,
                        key=lambda guest: sum(guest.get_preference(other) for other in table.guests if guest != other)
                    )
                )
        return centroids

    def run(self):
        """Run the K-Clustering algorithm to optimize the seating plan."""
        start_time = time.time()  # Start timing
        centroids = self.initialize_centroids()
        best_plan = None
        best_score = float('-inf')

        for _ in range(self.max_iterations):
            # Assign guests to tables based on current centroids
            tables = self.assign_guests_to_tables(centroids)

            # Create a seating plan and calculate its score
            seating_plan = SeatingPlan(self.guests, self.num_tables, self.table_capacity)
            seating_plan.tables = tables
            score = seating_plan.score()

            # Update the best plan if the score improves
            if score > best_score:
                best_plan = seating_plan
                best_score = score

            # Calculate new centroids
            new_centroids = self.calculate_new_centroids(tables)

            # Check for convergence (if centroids don't change)
            if all(new_centroids[i].name == centroids[i].name for i in range(len(centroids))):
                break

            centroids = new_centroids

        end_time = time.time()  # End timing
        execution_time = end_time - start_time  # Calculate execution time
        return best_plan, best_score, execution_time

