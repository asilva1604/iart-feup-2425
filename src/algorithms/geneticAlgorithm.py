import random
from seating_plan import SeatingPlan

class GeneticAlgorithm:
    def __init__(self, guests, num_tables, table_capacity, population_size=30, generations=50, mutation_rate=0.1, elitism_rate=0.1):
        """
        Initialize the Genetic Algorithm with all necessary parameters.

        Parameters:
        - guests: List of all guests.
        - num_tables: Total number of tables.
        - table_capacity: Maximum number of guests per table.
        - population_size: Number of solutions in each generation.
        - generations: Number of generations to evolve.
        - mutation_rate: Probability of mutation occurring.
        - elitism_rate: Proportion of best solutions carried forward unchanged.
        """
        self.guests = guests
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate
        self.fitness_cache = {}  # Memoization for fitness function to avoid recalculating

    def initialize_population(self):
        """Create the initial population with random seating plans."""
        return [SeatingPlan(self.guests, self.num_tables, self.table_capacity) for _ in range(self.population_size)]

    def fitness(self, seating_plan):
        """Compute and cache the fitness score of a seating plan."""
        plan_key = tuple(tuple(table.guests) for table in seating_plan.tables)
        if plan_key not in self.fitness_cache:
            self.fitness_cache[plan_key] = seating_plan.score()
        return self.fitness_cache[plan_key]

    def selection(self, population, fitness_scores):
        """
        Select one parent using tournament selection.

        This helps maintain diversity and selects fitter individuals more often.
        """
        tournament_size = 3
        selected = random.choices(population, k=tournament_size)
        selected_scores = [fitness_scores[population.index(ind)] for ind in selected]
        return selected[selected_scores.index(max(selected_scores))]

    def crossover(self, parent1, parent2):
        """
        Generate a child by combining tables from both parents.

        For each table, there's a 50% chance of inheriting it from parent2.
        """
        child = parent1.copy()
        for i in range(len(child.tables)):
            if random.random() < 0.5:
                child.tables[i].guests = parent2.tables[i].guests[:]  # Copy guest list
        return child

    def mutation(self, seating_plan):
        """
        Randomly mutate a seating plan by swapping two guests from different tables.

        This introduces genetic diversity and helps avoid local optima.
        """
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
        """Main loop for running the Genetic Algorithm and returning the best solution."""
        population = self.initialize_population()
        best_plan = None
        best_score = float('-inf')

        for gen in range(self.generations):
            # Calculate fitness scores for the current population
            fitness_scores = [self.fitness(plan) for plan in population]

            # Track the best solution found so far
            max_fitness_idx = fitness_scores.index(max(fitness_scores))
            if fitness_scores[max_fitness_idx] > best_score:
                best_plan = population[max_fitness_idx]
                best_score = fitness_scores[max_fitness_idx]

            # Apply elitism: carry forward a fraction of the best individuals
            num_elites = max(1, int(self.elitism_rate * self.population_size))
            elites = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)[:num_elites]
            next_generation = [elite[0] for elite in elites]

            # Generate remaining individuals for the next generation
            while len(next_generation) < self.population_size:
                parent1 = self.selection(population, fitness_scores)
                parent2 = self.selection(population, fitness_scores)
                child = self.crossover(parent1, parent2)
                self.mutation(child)
                next_generation.append(child)

            # Move to next generation
            population = next_generation

        return best_plan, best_score
