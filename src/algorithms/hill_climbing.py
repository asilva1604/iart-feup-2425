import random
from seating_plan import SeatingPlan, Table

class HillClimbing:
    def __init__(self, seating_plan, max_iterations=10000):
        self.current_plan = seating_plan
        self.best_plan = seating_plan
        self.current_score = seating_plan.score()
        self.best_score = self.current_score
        self.max_iterations = max_iterations

    def run(self):
        for _ in range(self.max_iterations):
            new_plan = self._generate_neighbor()
            new_score = new_plan.score()

            if new_score > self.current_score:
                self.current_plan = new_plan
                self.current_score = new_score

                if new_score > self.best_score:
                    self.best_plan = new_plan
                    self.best_score = new_score

        return self.best_plan, self.best_score

    def _generate_neighbor(self):
        """Generates a neighboring solution by swapping guests between tables."""
        new_plan = SeatingPlan(self.current_plan.guest_list, len(self.current_plan.tables), self.current_plan.tables[0].capacity)
        new_plan.tables = [Table(table.capacity) for table in self.current_plan.tables]
        for i, table in enumerate(self.current_plan.tables):
            new_plan.tables[i].guests = table.guests[:]

        table1, table2 = random.sample(range(len(new_plan.tables)), 2)
        new_plan.swap_guests(table1, table2)
        return new_plan