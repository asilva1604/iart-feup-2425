import random
from seating_plan import SeatingPlan

class GeneticAlgorithm:
    def __init__(self, guests, num_tables, table_capacity, population_size=30, generations=50, mutation_rate=0.1, elitism_rate=0.1):
        self.guests = guests
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate  # Percentage of top individuals to retain
        self.fitness_cache = {}  # Cache for fitness evaluations

    def initialize_population(self):
        """Initialize the population with random seating plans."""
        return [SeatingPlan(self.guests, self.num_tables, self.table_capacity) for _ in range(self.population_size)]

    def fitness(self, seating_plan):
        """Calculate the fitness (score) of a seating plan, using caching."""
        plan_key = tuple(tuple(table.guests) for table in seating_plan.tables)
        if plan_key not in self.fitness_cache:
            self.fitness_cache[plan_key] = seating_plan.score()
        return self.fitness_cache[plan_key]

    def selection(self, population, fitness_scores):
        """Select two parents using tournament selection."""
        tournament_size = 3
        selected = random.choices(population, k=tournament_size)
        selected_scores = [fitness_scores[population.index(ind)] for ind in selected]
        return selected[selected_scores.index(max(selected_scores))]

    def crossover(self, parent1, parent2):
        """Perform crossover between two parents to produce a child."""
        child = parent1.copy()
        for i in range(len(child.tables)):
            if random.random() < 0.5:
                child.tables[i].guests = parent2.tables[i].guests[:]
        return child

    def mutation(self, seating_plan):
        """Mutate a seating plan by swapping guests between tables."""
        if random.random() < self.mutation_rate:
            table1, table2 = random.sample(range(self.num_tables), 2)
            if seating_plan.tables[table1].guests and seating_plan.tables[table2].guests:
                guest1 = random.choice(seating_plan.tables[table1].guests)
                guest2 = random.choice(seating_plan.tables[table2].guests)
                seating_plan.tables[table1].remove_guest(guest1)
                seating_plan.tables[table2].remove_guest(guest2)
                seating_plan.tables[table1].add_guest(guest2)
                seating_plan.tables[table2].add_guest(guest1)

    def run(self):
        """Run the Genetic Algorithm to optimize the seating plan."""
        population = self.initialize_population()
        best_plan = None
        best_score = float('-inf')

        for gen in range(self.generations):
            # Evaluate fitness for the population
            fitness_scores = [self.fitness(plan) for plan in population]

            # Update the best solution
            max_fitness_idx = fitness_scores.index(max(fitness_scores))
            if fitness_scores[max_fitness_idx] > best_score:
                best_plan = population[max_fitness_idx]
                best_score = fitness_scores[max_fitness_idx]

            # Elitism: Retain the top individuals
            num_elites = max(1, int(self.elitism_rate * self.population_size))
            elites = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)[:num_elites]
            next_generation = [elite[0] for elite in elites]

            # Generate the rest of the next generation
            while len(next_generation) < self.population_size:
                parent1 = self.selection(population, fitness_scores)
                parent2 = self.selection(population, fitness_scores)
                child = self.crossover(parent1, parent2)
                self.mutation(child)
                next_generation.append(child)

            population = next_generation

        return best_plan, best_score

