import math
import random
from seating_plan import SeatingPlan

class SimulatedAnnealing:
    def __init__(self, seating_plan, initial_temp=10000, cooling_rate=0.99, iterations=10000):
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
        # Create a deep copy of the current plan
        new_plan = self.current_plan.copy()  # Assuming a copy method exists
        
        # Select two tables randomly
        table1, table2 = random.sample(range(len(new_plan.tables)), 2)
        
        # Select one random guest from each table
        if new_plan.tables[table1].guests and new_plan.tables[table2].guests:
            guest1 = random.choice(new_plan.tables[table1].guests)
            guest2 = random.choice(new_plan.tables[table2].guests)
            
            # Swap the selected guests
            new_plan.move_guest(guest1, table1, table2)
            new_plan.move_guest(guest2, table2, table1)
        
        return new_plan