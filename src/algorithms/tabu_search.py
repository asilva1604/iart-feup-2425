import random
from seating_plan import SeatingPlan, Table

class TabuSearch:
    def __init__(self, seating_plan, tabu_tenure=5, max_iterations=1000):
        self.current_plan = seating_plan
        self.best_plan = seating_plan
        self.current_score = seating_plan.score()
        self.best_score = self.current_score
        self.tabu_list = []
        self.tabu_tenure = tabu_tenure
        self.max_iterations = max_iterations

    def run(self):
        for _ in range(self.max_iterations):
            neighborhood = self._generate_neighbors()
            best_neighbor = None
            best_neighbor_score = float('-inf')

            for neighbor in neighborhood:
                if neighbor not in self.tabu_list:
                    neighbor_score = neighbor.score()
                    if neighbor_score > best_neighbor_score:
                        best_neighbor = neighbor
                        best_neighbor_score = neighbor_score

            if best_neighbor:
                self.current_plan = best_neighbor
                self.current_score = best_neighbor_score

                if self.current_score > self.best_score:
                    self.best_plan = self.current_plan
                    self.best_score = self.current_score

                self.tabu_list.append(self.current_plan)
                if len(self.tabu_list) > self.tabu_tenure:
                    self.tabu_list.pop(0)

        return self.best_plan, self.best_score

    def _generate_neighbors(self):
        """Generates neighboring solutions by swapping guests between tables."""
        neighbors = []
        for _ in range(10):  # Generate 10 neighbors
            new_plan = SeatingPlan(self.current_plan.guest_list, len(self.current_plan.tables), self.current_plan.tables[0].capacity)
            new_plan.tables = [Table(table.capacity) for table in self.current_plan.tables]
            for i, table in enumerate(self.current_plan.tables):
                new_plan.tables[i].guests = table.guests[:]

            table1, table2 = random.sample(range(len(new_plan.tables)), 2)
            new_plan.swap_guests(table1, table2)
            neighbors.append(new_plan)
        return neighbors