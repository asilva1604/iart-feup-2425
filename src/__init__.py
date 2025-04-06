import time
from algorithms import SimulatedAnnealing, HillClimbing, Greedy, TabuSearch, GeneticAlgorithm, KClustering
from seating_plan import SeatingPlan

def run_all_algorithms(guests, num_tables, table_capacity):
    """Runs all algorithms and returns their results."""
    results = []
    seating_plan = SeatingPlan(guests, num_tables=num_tables, table_capacity=table_capacity)

    # Simulated Annealing
    start_time = time.time()
    optimizer = SimulatedAnnealing(seating_plan)
    best_plan, best_score = optimizer.run()
    end_time = time.time()
    results.append(['Simulated Annealing', best_score, end_time - start_time, best_plan])

    # Hill Climbing
    start_time = time.time()
    optimizer = HillClimbing(seating_plan)
    best_plan, best_score = optimizer.run()
    end_time = time.time()
    results.append(['Hill Climbing', best_score, end_time - start_time, best_plan])

    # Greedy
    start_time = time.time()
    optimizer = Greedy(guests, num_tables=num_tables, table_capacity=table_capacity)
    best_plan = optimizer.run()
    best_score = sum(
        guest.get_preference(other)
        for table in best_plan
        for guest in table.guests
        for other in table.guests
        if guest != other
    )
    end_time = time.time()
    results.append(['Greedy', best_score, end_time - start_time, best_plan])

    # Tabu Search
    start_time = time.time()
    optimizer = TabuSearch(seating_plan)
    best_plan, best_score = optimizer.run()
    end_time = time.time()
    results.append(['Tabu Search', best_score, end_time - start_time, best_plan])

    # Genetic Algorithm
    start_time = time.time()
    optimizer = GeneticAlgorithm(guests, num_tables=num_tables, table_capacity=table_capacity)
    best_plan, best_score = optimizer.run()
    end_time = time.time()
    results.append(['Genetic Algorithm', best_score, end_time - start_time, best_plan])

    # K-Clustering
    start_time = time.time()
    optimizer = KClustering(guests, num_tables=num_tables, table_capacity=table_capacity)
    k_clustering_result = optimizer.run()  # Handle multiple return values
    best_plan, best_score, execution_time = k_clustering_result
    results.append(['K-Clustering', best_score, execution_time, best_plan])

    return results

