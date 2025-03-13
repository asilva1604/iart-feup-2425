from seating_plan import Table

class Greedy:
    def __init__(self, guests, num_tables, table_capacity):
        self.tables = [Table(table_capacity) for _ in range(num_tables)]
        self.guest_list = guests

    def run(self):
        # Sort guests by the sum of their preferences, and use the guest's name as a secondary criterion
        sorted_guests = sorted(self.guest_list, key=lambda x: (sum(x.preferences.values()), x.name), reverse=True)

        for guest in sorted_guests:
            best_table = None
            best_score = float('-inf')
            for table in self.tables:
                if not table.is_full():
                    score = sum(guest.get_preference(other) for other in table.guests)
                    if score > best_score:
                        best_table = table
                        best_score = score
            if best_table:
                best_table.add_guest(guest)
        return self.tables