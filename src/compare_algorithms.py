import matplotlib.pyplot as plt
from __init__ import run_all_algorithms
from utils import read_input_csv
import os

def compare_algorithms(input_file, num_tables, table_capacity):
    """Run all algorithms and generate comparison graphs."""
    # Read input data
    guests = read_input_csv(input_file)
    
    # Run all algorithms
    results = run_all_algorithms(guests, num_tables, table_capacity)
    
    # Extract data for plotting
    algorithms = [result[0] for result in results]
    best_scores = [result[1] for result in results]
    execution_times = [result[2] for result in results]
    score_to_time_ratios = [score / time if time > 0 else 0 for score, time in zip(best_scores, execution_times)]
    score_progressions = [result[3] for result in results]  # Histórico de progresso das soluções
    
    # Plot best scores
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, best_scores, color="skyblue")
    plt.title("Algorithm Comparison - Best Scores")
    plt.ylabel("Best Score")
    plt.xlabel("Algorithm")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("best_scores_comparison.png")
    plt.show()
    
    # Plot execution times
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, execution_times, color="lightcoral")
    plt.title("Algorithm Comparison - Execution Time")
    plt.ylabel("Execution Time (s)")
    plt.xlabel("Algorithm")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("execution_time_comparison.png")
    plt.show()

    # Plot score-to-time ratio
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, score_to_time_ratios, color="lightgreen")
    plt.title("Algorithm Comparison - Score-to-Time Ratio")
    plt.ylabel("Score-to-Time Ratio")
    plt.xlabel("Algorithm")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("score_to_time_ratio_comparison.png")
    plt.show()

    # Line plot for best scores and execution times
    plt.figure(figsize=(10, 5))
    plt.plot(algorithms, best_scores, marker='o', label="Best Scores", color="blue")
    plt.plot(algorithms, execution_times, marker='o', label="Execution Time (s)", color="red")
    plt.title("Algorithm Comparison - Line Plot")
    plt.ylabel("Values")
    plt.xlabel("Algorithm")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("line_plot_comparison.png")
    plt.show()

    # Scatter plot for execution time vs. best scores
    plt.figure(figsize=(10, 5))
    plt.scatter(execution_times, best_scores, color="purple", s=100)
    for i, algorithm in enumerate(algorithms):
        plt.text(execution_times[i], best_scores[i], algorithm, fontsize=9, ha='right')
    plt.title("Execution Time vs. Best Scores")
    plt.xlabel("Execution Time (s)")
    plt.ylabel("Best Score")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("scatter_plot_comparison.png")
    plt.show()
    
    # NEW: Line plot showing the progression of scores over iterations
    plt.figure(figsize=(10, 5))
    for algo, scores in zip(algorithms, score_progressions):
        if isinstance(scores, list) and all(isinstance(score, (int, float)) for score in scores):
            plt.plot(range(len(scores)), scores, label=algo)
        else:
            print(f"Warning: Skipping {algo} due to invalid score progression data.")

    plt.xlabel("Iterations")
    plt.ylabel("Best Score Over Time")
    plt.title("Algorithm Performance Over Iterations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("algorithm_progression.png")
    plt.show()

if __name__ == "__main__":
    # Example usage
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(BASE_DIR, "small.csv")  # Change to your dataset file
    num_tables = 5
    table_capacity = 3
    
    compare_algorithms(input_file, num_tables, table_capacity)

import numpy as np
import matplotlib.pyplot as plt

# Simulando o desempenho dos algoritmos ao longo do tempo
np.random.seed(42)
iterations = 100
algorithms = {
    "Hill Climbing": np.cumsum(np.random.rand(iterations) * 2),
    "Simulated Annealing": np.cumsum(np.random.rand(iterations) * 1.8),
    "Tabu Search (5)": np.cumsum(np.random.rand(iterations) * 2.2),
    "Tabu Search (10)": np.cumsum(np.random.rand(iterations) * 2.0),
    "Genetic Algorithm": np.full(iterations, np.max(np.cumsum(np.random.rand(iterations) * 2.5)))  # Estabiliza no topo
}

# Criando o gráfico
plt.figure(figsize=(10, 5))
for algo, scores in algorithms.items():
    plt.plot(scores, label=algo)

# Ajustando o gráfico
plt.xlabel("Iterações")
plt.ylabel("Melhor Pontuação")
plt.title("Comparação de Algoritmos de Otimização")
plt.legend()
plt.grid(True)
plt.show()
