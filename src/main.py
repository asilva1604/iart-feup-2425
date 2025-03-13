from algorithms import SimulatedAnnealing, HillClimbing, Greedy, BruteForce, TabuSearch
from seating_plan import SeatingPlan, Guest
# Define guests
guests = [Guest(f"Guest{i}") for i in range(1, 90)]

# Define preferences (higher = wants to sit together, lower = should be apart)
import random

for guest in guests:
    for other_guest in guests:
        if guest != other_guest:
            guest.set_preference(other_guest, random.randint(-10, 10))

# Create initial seating plan with new guests
seating_plan = SeatingPlan(guests, num_tables=31, table_capacity=3)
print("Initial Seating Plan:\n", seating_plan)
print("Initial Score:", seating_plan.score())

# Optimize with Simulated Annealing
optimizer = SimulatedAnnealing(seating_plan)
best_plan, best_score = optimizer.run()

print("\nSimulated Annealing Optimized Seating Plan:\n", best_plan)
print("Best Score:", best_score)

hill_climbing = HillClimbing(seating_plan)
best_plan1, best_score1 = hill_climbing.run()

print("\nHill Climbing Optimized Seating Plan1:\n", best_plan1)
print("Best Score1:", best_score1)

greedy = Greedy(guests, num_tables=10, table_capacity=3)
best_greedy_plan = greedy.run()

print("\nGreedy Seating Plan:\n")
for table in best_greedy_plan:
    print(table)

total_score = sum(guest.get_preference(other) for table in best_greedy_plan for guest in table.guests for other in table.guests if guest != other)
print("Total Score:", total_score)

tabu_search = TabuSearch(seating_plan)
best_tabu_plan, best_tabu_score = tabu_search.run()

print("\nTabu Search Optimized Seating Plan:\n", best_tabu_plan)
print("Best Tabu Search Score:", best_tabu_score)

# Example usage
#brute_force = BruteForce(guests, num_tables=10, table_capacity=3)
#best_brute_force_plan, best_brute_force_score = brute_force.run()

#print("\nBrute Force Optimized Seating Plan:\n", best_brute_force_plan)
#print("Best Brute Force Score:", best_brute_force_score)