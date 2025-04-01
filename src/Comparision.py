import pandas as pd
import matplotlib.pyplot as plt
import time
from algorithms import SimulatedAnnealing,  HillClimbing, BruteForce, GeneticAlgorithm, Greedy, tabu_search
from seating_plan import SeatingPlan
from utils import read_input_csv

filepath = "input.csv"

def compare_algorithms(filepath, num_tables, table_capacity):
    guests = read_input_csv(filepath)
    seating_plan = SeatingPlan(guests, num_tables, table_capacity)

    result = []

    # Simulated Annealing
    start_time = time.time()
    optimizer = SimulatedAnnealing(seating_plan)
    best_plan, best_scorez = optimizer.run()
    end_time = time.time()
    result.append(["Simulated Annealing", best_scorez, end_time - start_time])

    # Hill Climbing
    start_time = time.time()
    optimizer = HillClimbing(seating_plan)
    best_plan, best_scorez = optimizer.run()
    end_time = time.time()
    result.append(["Hill CLimbing", best_scorez, end_time - start_time])


    # Simulated Annealing
    start_time = time.time()
    optimizer = BruteForce(seating_plan)
    best_plan, best_scorez = optimizer.run()
    end_time = time.time()
    result.append(["Simulated Annealing", best_scorez, end_time - start_time])



    # Simulated Annealing
    start_time = time.time()
    optimizer = GeneticAlgorithm(seating_plan)
    best_plan, best_scorez = optimizer.run()
    end_time = time.time()
    result.append(["Simulated Annealing", best_scorez, end_time - start_time])


    # Simulated Annealing
    start_time = time.time()
    optimizer = Greedy(seating_plan)
    best_plan, best_scorez = optimizer.run()
    end_time = time.time()
    result.append(["Simulated Annealing", best_scorez, end_time - start_time])

    start_time = time.time()
    optimizer = tabu_search(seating_plan)
    best_plan, best_scorez = optimizer.run()
    end_time = time.time()
    result.append(["Simulated Annealing", best_scorez, end_time - start_time])

def plot_comparison(df):

    plt.figure(figsize=(10, 5))
    plt.bar(df["Algorithm"], df["Best Score"], color="skyblue")
    plt.title("Algorithm Comparison - Best Scores")
    plt.title("Best Score")
    plt.ylabel("Algorithm")
    plt.xlabel(rotation=45)
    plt.tight_layout()
    plt.show()


    plt.figure(figsize=(10, 5))
    plt.bar(df["Algorithm"], df["Execution Time (s)"], color="lightcoral")
    plt.title("Algorithm Comparison - Execution Time")
    plt.title("Execution Time (s)")
    plt.ylabel("Algorithm")
    plt.xlabel(rotation=45)
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    num_tables = 5
    table_capacity = 3

    df = compare_algorithms(filepath, num_tables, table_capacity) 
    print(df)

    plot_comparison(df)