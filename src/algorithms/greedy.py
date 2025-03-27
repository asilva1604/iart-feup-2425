from seating_plan import Table

class Greedy:
    def __init__(self, guests, num_tables, table_capacity):
        self.tables = [Table(table_capacity) for _ in range(num_tables)]
        self.guest_list = guests

    def run(self):
        # Sort guests by the sum of their top-k preferences to improve grouping
        def preference_score(guest, k=3):
            return sum(sorted(guest.preferences.values(), reverse=True)[:k])
        
        sorted_guests = sorted(self.guest_list, key=lambda x: (preference_score(x), x.name), reverse=True)
        
        # Distribute guests initially to avoid empty tables
        for i, guest in enumerate(sorted_guests[:len(self.tables)]):
            self.tables[i].add_guest(guest)
        
        # Assign remaining guests using a better heuristic
        for guest in sorted_guests[len(self.tables):]:
            best_table = None
            best_score = float('-inf')
            
            for table in self.tables:
                if not table.is_full():
                    score = sum(guest.get_preference(other) for other in table.guests)
                    if score > best_score:
                        best_table = table
                        best_score = score
            
            # If a table was found, place the guest there
            if best_table:
                best_table.add_guest(guest)
            else:
                # Handle the case where all tables are full (should not happen normally)
                raise ValueError("All tables are full before all guests were seated. Consider increasing table capacity or number of tables.")
        
        return self.tables
