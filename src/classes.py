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
    
import math
import random

class SimulatedAnnealing:
    def __init__(self, seating_plan, initial_temp=1000, cooling_rate=0.995, iterations=10000):
        self.current_plan = seating_plan
        self.best_plan = seating_plan
        self.current_score = seating_plan.score()
        self.best_score = self.current_score
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.iterations = iterations

    def run(self):
        for i in range(self.iterations):
            new_plan = self._generate_neighbor()
            new_score = new_plan.score()
            delta = new_score - self.current_score

            if delta > 0 or math.exp(delta / self.temp) > random.random():
                self.current_plan = new_plan
                self.current_score = new_score

            if self.current_score > self.best_score:
                self.best_plan = self.current_plan
                self.best_score = self.current_score

            self.temp *= self.cooling_rate  # Reduce temperature

        return self.best_plan, self.best_score

    def _generate_neighbor(self):
        """Generates a neighboring solution by swapping guests between tables."""    
        new_plan = SeatingPlan(self.current_plan.guest_list, len(self.current_plan.tables), self.current_plan.tables[0].capacity)
        table1, table2 = random.sample(range(len(new_plan.tables)), 2)
        new_plan.swap_guests(table1, table2)
        return new_plan
    
class HillClimbing:
    def __init__(self, seating_plan, max_iterations=10000):
        self.current_plan = seating_plan
        self.best_plan = seating_plan
        self.current_score = seating_plan.score()
        self.best_score = self.current_score
        self.maxiterations = max_iterations

    def run(self):
        for _ in range(self.maxiterations):
            new_plan = self._generate_neighbor()
            new_score = new_plan.score()


            if new_score > self.current_score:
                self.current_plan = new_plan
                self.current_score = new_score

                if new_score > self.best_score:
                    self.best_plan = new_plan
                    self.best_score = new_score
            else:
                break

        return self.best_plan, self.best_score

    def _generate_neighbor(self):
        """Generates a neighboring solution by swapping guests between tables."""    
        new_plan = SeatingPlan(self.current_plan.guest_list, len(self.current_plan.tables), self.current_plan.tables[0].capacity)
        table1, table2 = random.sample(range(len(new_plan.tables)), 2)
        new_plan.swap_guests(table1, table2)
        return new_plan


class Greedy:
    def __init__(self, guests, num_tables, table_capacity):
        self.tables = [Table(table_capacity) for _ in range(num_tables)]
        self.guest_list = guests

    def run(self):

        sorted_guests = sorted(self.guest_list, key=lambda x: sum(x.preferences.values()), reverse=True)

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



# Define guests
alice = Guest("Alice")
bob = Guest("Bob")
charlie = Guest("Charlie")
david = Guest("David")

# Define preferences (higher = wants to sit together, lower = should be apart)
alice.set_preference(bob, 10)
alice.set_preference(charlie, -5)
bob.set_preference(charlie, 5)
bob.set_preference(david, 8)

guests = [alice, bob, charlie, david]

# Create initial seating plan
seating_plan = SeatingPlan(guests, num_tables=2, table_capacity=2)
print("Initial Seating Plan:\n", seating_plan)
print("Initial Score:", seating_plan.score())

# Optimize with Simulated Annealing
optimizer = SimulatedAnnealing(seating_plan)
best_plan, best_score = optimizer.run()

print("\nOptimized Seating Plan:\n", best_plan)
print("Best Score:", best_score)

hill_climbing = HillClimbing(seating_plan)
best_plan1, best_score1 = hill_climbing.run()

print("\nOptimized Seating Plan1:\n", best_plan1)
print("Best Score1:", best_score1)

greedy = Greedy(guests, num_tables=2, table_capacity=2)
best_greedy_plan = greedy.run()

print("\nGreedy Seating Plan:\n")
for table in best_greedy_plan:
    print(table)

total_score = sum(guest.get_preference(other) for table in best_greedy_plan for guest in table.guests for other in table.guests if guest != other)
print("Total Score:", total_score)
