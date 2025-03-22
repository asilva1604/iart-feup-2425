import random
from seating_plan import SeatingPlan


class GeneticAlgorithm:
    def __init__(self, guests, num_tables, table_capacity, population_size=50, generations=100, mutation_rate=0.1):
        self.guests = guests
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        self.population = [SeatingPlan(self.guests,self.num_tables,self.table_capacity) for _ in range(self.population_size)]
        return self.population

    def fitness(self, seating_plan):
        return seating_plan.score()
    
    def selection(self, population):
        fitness_score = [self.fitness(plan) for plan in population]
        total_fitness = sum(fitness_score)
        if total_fitness == 0:
            return random.sample(population, 2)
        prob = [score / total_fitness for score in fitness_score]
        return random.choices(population, weights=prob, k=2)
    
    def crossover(self, parent1, parent2):
        child = parent1.copy()
        for i in range(len(child.tables)):
            if random.random() < 0.5:
                child.tables[i].guests = parent2.tables[i].guests[:]
        return child
    
    def mutation(self, seating_plan):
        if random.random() < self.mutation_rate:
            table1, table2 = random.sample(range(self.num_tables), 2)
            if seating_plan.tables[table1].guests:
                guest = random.choice(seating_plan.tables[table1].guests)
                seating_plan.move_guest(guest, table1, table2)

    def run(self):
        population = self.initialize_population()
        best_plan = None
        best_score = float('-inf')

        for gen in range(self.generations):
            population = sorted(population, key=self.fitness, reverse=True)
            if self.fitness(population[0]) > best_score:
                best_plan = population[0]
                best_score = self.fitness(best_plan)
            
            next_generation = []
            while len(next_generation) < self.population_size:
                parent1, parent2 = self.selection(population)
                child = self.crossover(parent1, parent2)
                self.mutation(child)
                next_generation.append(child)

            population = next_generation

            if best_plan is None:
                best_plan = population[0]

        return best_plan, best_score

        