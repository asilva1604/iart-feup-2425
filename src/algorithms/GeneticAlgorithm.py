import random
from seating_plan import SeatingPlan


class GeneticAlgorithm:
    def __init__(self, guest, num_tables, table_capacity, population_size=50, generations=100, mutation_rate=0.1):
        self.guest = guest
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        self.population = [SeatingPlan(self.guest,self.num_tables,self.table_capacity) for _ in range(self.population_size)]
        