import time
from algorithms import SimulatedAnnealing, HillClimbing, Greedy, BruteForce, TabuSearch, GeneticAlgorithm 
from seating_plan import SeatingPlan, Guest
from utils import read_input_csv, write_output_csv

# Read input CSV
input_file_path = './input.csv'
guests = read_input_csv(input_file_path)

# Calculate the number of tables required
table_capacity = 3
num_tables = (len(guests) + table_capacity - 1) // table_capacity  # Ceiling division

# Create initial seating plan with new guests
seating_plan = SeatingPlan(guests, num_tables=num_tables, table_capacity=table_capacity)
print("Initial Seating Plan:\n", seating_plan)
print("Initial Score:", seating_plan.score())

results = []

# Optimize with Simulated Annealing
start_time = time.time()
optimizer = SimulatedAnnealing(seating_plan)
best_plan, best_score = optimizer.run()
end_time = time.time()
time_taken = end_time - start_time
results.append(['Simulated Annealing', best_score, time_taken, best_plan])

print("\nSimulated Annealing Optimized Seating Plan:\n", best_plan)
print("Best Score:", best_score)

# Optimize with Hill Climbing
start_time = time.time()
hill_climbing = HillClimbing(seating_plan)
best_plan1, best_score1 = hill_climbing.run()
end_time = time.time()
time_taken = end_time - start_time
results.append(['Hill Climbing', best_score1, time_taken, best_plan1])

print("\nHill Climbing Optimized Seating Plan1:\n", best_plan1)
print("Best Score1:", best_score1)

# Optimize with Greedy
start_time = time.time()
greedy = Greedy(guests, num_tables=num_tables, table_capacity=table_capacity)
best_greedy_plan = greedy.run()
end_time = time.time()
time_taken = end_time - start_time
total_score = sum(guest.get_preference(other) for table in best_greedy_plan for guest in table.guests for other in table.guests if guest != other)
results.append(['Greedy', total_score, time_taken, best_greedy_plan])

print("\nGreedy Seating Plan:\n")
for table in best_greedy_plan:
    print(table)

print("Total Score:", total_score)

# Optimize with Tabu Search
start_time = time.time()
tabu_search = TabuSearch(seating_plan)
best_tabu_plan, best_tabu_score = tabu_search.run()
end_time = time.time()
time_taken = end_time - start_time
results.append(['Tabu Search', best_tabu_score, time_taken, best_tabu_plan])

print("\nTabu Search Optimized Seating Plan:\n", best_tabu_plan)
print("Best Tabu Search Score:", best_tabu_score)

# Optimize with Brute Force
start_time = time.time()
brute_force = BruteForce(guests, num_tables=num_tables, table_capacity=table_capacity)
best_brute_force_plan, best_brute_force_score = brute_force.run()
end_time = time.time()
time_taken = end_time - start_time
results.append(['Brute Force', best_brute_force_score, time_taken, best_brute_force_plan])

print("\nBrute Force Optimized Seating Plan:\n", best_brute_force_plan)
print("Best Brute Force Score:", best_brute_force_score)

# Optimize with Genetic Algorithm
start_time = time.time()
genetic_algorithm = GeneticAlgorithm(guests, num_tables=num_tables, table_capacity=table_capacity)
best_ga_plan, best_ga_score = genetic_algorithm.run()
end_time = time.time()
time_taken = end_time - start_time
results.append(['Genetic Algorithm', best_ga_score, time_taken, best_ga_plan])

print("\nGenetic Algorithm Optimized Seating Plan:\n", best_ga_plan)
print("Best Genetic Algorithm Score:", best_ga_score)

# Write output CSV
output_file_path = 'output.csv'
write_output_csv(output_file_path, results)