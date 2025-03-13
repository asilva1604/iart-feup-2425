class Guest:
    def __init__(self, name):
        self.name = name
        self.preferences = {}  # Dictionary of guest -> preference score

    def set_preference(self, other_guest, score):
        self.preferences[other_guest] = score

    def get_preference(self, other_guest):
        return self.preferences.get(other_guest, 0)

    def __repr__(self):
        return self.name

class Table:
    def __init__(self, capacity):
        self.capacity = capacity
        self.guests = []

    def add_guest(self, guest):
        if len(self.guests) < self.capacity:
            self.guests.append(guest)
            return True
        return False

    def remove_guest(self, guest):
        if guest in self.guests:
            self.guests.remove(guest)

    def is_full(self):
        return len(self.guests) >= self.capacity

    def __repr__(self):
        return f"Table({self.guests})"
    
class SeatingPlan:
    def __init__(self, guests, num_tables, table_capacity):
        self.tables = [Table(table_capacity) for _ in range(num_tables)]
        self.guest_list = guests
        self.assign_guests_randomly()

    def assign_guests_randomly(self):
        import random
        random.shuffle(self.guest_list)
        table_idx = 0
        for guest in self.guest_list:
            while not self.tables[table_idx].add_guest(guest):
                table_idx = (table_idx + 1) % len(self.tables)  # Move to the next table

    def score(self):
        """Calculates the total preference score of the seating plan."""
        total_score = 0
        for table in self.tables:
            for guest in table.guests:
                for other in table.guests:
                    if guest != other:
                        total_score += guest.get_preference(other)
        return total_score

    def swap_guests(self, table1_idx, table2_idx):
        """Swaps a guest between two tables."""
        import random
        if not self.tables[table1_idx].guests or not self.tables[table2_idx].guests:
            return
        g1 = random.choice(self.tables[table1_idx].guests)
        g2 = random.choice(self.tables[table2_idx].guests)
        self.tables[table1_idx].remove_guest(g1)
        self.tables[table2_idx].remove_guest(g2)
        self.tables[table1_idx].add_guest(g2)
        self.tables[table2_idx].add_guest(g1)

    def __repr__(self):
        return "\n".join(str(table) for table in self.tables)