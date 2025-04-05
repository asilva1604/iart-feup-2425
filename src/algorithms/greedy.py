from seating_plan import Table

# Define the Greedy class, which assigns guests to tables using a greedy heuristic
class Greedy:
    def __init__(self, guests, num_tables, table_capacity):
        # Create a list of Table objects based on the given number of tables and capacity
        self.tables = [Table(table_capacity) for _ in range(num_tables)]
        # Store the list of guests
        self.guest_list = guests

    # Main method that executes the seating algorithm
    def run(self):
        # Define a helper function that calculates a preference score for a guest
        # based on the sum of their top-k preferences (default k=3)
        def preference_score(guest, k=3):
            return sum(sorted(guest.preferences.values(), reverse=True)[:k])
        
        # Sort guests by their preference score (and by name as a tiebreaker)
        # Higher scores come first
        sorted_guests = sorted(self.guest_list, key=lambda x: (preference_score(x), x.name), reverse=True)
        
        # Distribute the first few guests across tables to avoid empty tables
        for i, guest in enumerate(sorted_guests[:len(self.tables)]):
            self.tables[i].add_guest(guest)
        
        # Assign the remaining guests using a heuristic
        for guest in sorted_guests[len(self.tables):]:
            best_table = None
            best_score = float('-inf')
            
            # Evaluate each table to find where the guest would fit best
            for table in self.tables:
                if not table.is_full():
                    # Compute the sum of this guest's preferences for people already at the table
                    score = sum(guest.get_preference(other) for other in table.guests)
                    # Update the best table if this one has a higher score
                    if score > best_score:
                        best_table = table
                        best_score = score
            
            # If a suitable table was found, add the guest to it
            if best_table:
                best_table.add_guest(guest)
            else:
                # If all tables are full (should not happen), raise an error
                raise ValueError("All tables are full before all guests were seated. Consider increasing table capacity or number of tables.")
        
        # Return the final list of tables with seated guests
        return self.tables