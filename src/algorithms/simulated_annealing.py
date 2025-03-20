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
        new_plan = self.current_plan.copy()
        
        # Choose a random neighbor generation strategy
        strategy = random.choice(['swap', 'move', 'reassign_multiple'])
        
        # Get non-empty tables
        non_empty_tables = [i for i, table in enumerate(new_plan.tables) if table.guests]
        
        # If we have no guests at all, return the unchanged plan
        if not non_empty_tables:
            return new_plan
            
        if strategy == 'swap' and len(non_empty_tables) >= 2:
            # Swap guests between two tables
            table1, table2 = random.sample(non_empty_tables, 2)
            guest1 = random.choice(new_plan.tables[table1].guests)
            guest2 = random.choice(new_plan.tables[table2].guests)
            new_plan.move_guest(guest1, table1, table2)
            new_plan.move_guest(guest2, table2, table1)
            
        elif strategy == 'move' or len(non_empty_tables) < 2:
            # Move a guest to a different table
            source_table = random.choice(non_empty_tables)
            guest = random.choice(new_plan.tables[source_table].guests)
            possible_tables = [i for i in range(len(new_plan.tables)) if i != source_table]
            if possible_tables:  # Make sure there's at least one other table
                target_table = random.choice(possible_tables)
                new_plan.move_guest(guest, source_table, target_table)
                
        elif strategy == 'reassign_multiple':
            # Reassign multiple guests (more aggressive exploration)
            num_moves = random.randint(1, max(3, len(non_empty_tables) // 2))
            for _ in range(num_moves):
                if not non_empty_tables:  # Check if we still have non-empty tables
                    break
                source_table = random.choice(non_empty_tables)
                if not new_plan.tables[source_table].guests:  # Check if table still has guests
                    non_empty_tables.remove(source_table)
                    continue
                guest = random.choice(new_plan.tables[source_table].guests)
                possible_tables = [i for i in range(len(new_plan.tables)) if i != source_table]
                if possible_tables:
                    target_table = random.choice(possible_tables)
                    new_plan.move_guest(guest, source_table, target_table)
                    # Update non_empty_tables if needed
                    if not new_plan.tables[source_table].guests:
                        non_empty_tables.remove(source_table)
                    if target_table not in non_empty_tables:
                        non_empty_tables.append(target_table)
        
        return new_plan