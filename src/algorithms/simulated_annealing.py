import math
import random
import logging
import time
from seating_plan import SeatingPlan

# Configure logging for debug and progress info
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimulatedAnnealing:
    def __init__(self, seating_plan, initial_temp=1000, cooling_rate=0.99, iterations=30000):
        self.current_plan = seating_plan
        self.best_plan = seating_plan.copy()
        self.current_score = seating_plan.score()
        self.best_score = self.current_score

        # Simulated annealing hyperparameters
        self.initial_temp = initial_temp
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.iterations = iterations

        # Plateau handling
        self.no_improvement_count = 0
        self.max_no_improvement = 1000
        self.plateau_cooldown_factor = 0.8
        self.reheat_factor = 1.5

        # For analysis and debugging
        self.history = []  # Stores (iteration, score, temperature)
        self.perturbation_stats = {
            'swap': {'attempts': 0, 'improvements': 0},
            'move': {'attempts': 0, 'improvements': 0},
            'reassign_cluster': {'attempts': 0, 'improvements': 0},
            'table_shuffle': {'attempts': 0, 'improvements': 0},
            'targeted_move': {'attempts': 0, 'improvements': 0}
        }

    def run(self):
        """Main optimization loop."""
        start_time = time.time()
        logging.info(f"Starting optimization with initial score: {self.current_score}")
        logging.info(f"Parameters: T={self.initial_temp}, cooling_rate={self.cooling_rate}, iterations={self.iterations}")

        self.history.append((0, self.current_score, self.temp))  # Record initial state

        for i in range(self.iterations):
            # If stuck too long, handle plateau
            if self.no_improvement_count > self.max_no_improvement:
                self._handle_optimization_plateau()
            
            # Choose which neighbor generation strategy to use
            strategy = self._select_perturbation_strategy(i)

            # Generate a neighbor plan using selected strategy
            new_plan, strategy_used = self._generate_neighbor(strategy)
            new_score = new_plan.score()
            delta = new_score - self.current_score

            # Update stats
            self.perturbation_stats[strategy_used]['attempts'] += 1

            # Determine if we accept the neighbor
            accept = False
            if delta > 0:  # Better solution
                accept = True
                self.perturbation_stats[strategy_used]['improvements'] += 1
                self.no_improvement_count = 0
            elif math.exp(delta / self.temp) > random.random():  # Worse, but accepted probabilistically
                accept = True
                self.no_improvement_count += 1
            else:  # Rejected
                self.no_improvement_count += 1

            if accept:
                self.current_plan = new_plan
                self.current_score = new_score
                # Update best solution
                if self.current_score > self.best_score:
                    self.best_plan = self.current_plan.copy()
                    self.best_score = self.current_score
                    logging.info(f"New best solution found: score = {self.best_score}")

            # Update temperature
            self.temp = self._cooling_schedule(i)

            # Periodic logging
            if i % 200 == 0 or i == self.iterations - 1:
                elapsed = time.time() - start_time
                self.history.append((i, self.current_score, self.temp))
                logging.info(
                    f"Iteration {i}/{self.iterations} ({(i/self.iterations*100):.1f}%) - "
                    f"Temp: {self.temp:.4f}, Current: {self.current_score:.2f}, "
                    f"Best: {self.best_score:.2f}, Elapsed: {elapsed:.1f}s"
                )

        # Final report
        self._log_final_stats(time.time() - start_time)
        return self.best_plan, self.best_score

    def _cooling_schedule(self, iteration):
        """Custom non-linear cooling schedule."""
        progress = iteration / self.iterations
        return self.initial_temp * (self.cooling_rate ** (1 + 2 * progress))

    def _handle_optimization_plateau(self):
        """Handle no improvement for a while by either reheating or cooling aggressively."""
        self.no_improvement_count = 0  # reset
        if random.random() < 0.7:
            self.temp *= self.plateau_cooldown_factor  # cool further
            logging.info(f"Plateau detected: cooling faster, new temp = {self.temp:.4f}")
        else:
            self.temp *= self.reheat_factor  # reheat to escape local optima
            logging.info(f"Plateau detected: reheating, new temp = {self.temp:.4f}")

    def _select_perturbation_strategy(self, iteration):
        """Dynamically select perturbation strategy depending on the phase of optimization."""
        if iteration < self.iterations * 0.3:
            return random.choices(
                ['swap', 'move', 'reassign_cluster', 'table_shuffle', 'targeted_move'],
                weights=[0.3, 0.3, 0.2, 0.1, 0.1]
            )[0]
        elif iteration < self.iterations * 0.7:
            return random.choices(
                ['swap', 'move', 'reassign_cluster', 'table_shuffle', 'targeted_move'],
                weights=[0.25, 0.25, 0.2, 0.15, 0.15]
            )[0]
        else:
            return random.choices(
                ['swap', 'move', 'reassign_cluster', 'table_shuffle', 'targeted_move'],
                weights=[0.35, 0.3, 0.15, 0.1, 0.1]
            )[0]

    def _calculate_table_score(self, plan, table_idx):
        """Helper to compute total preference score at one table."""
        score = 0
        table = plan.tables[table_idx]
        for guest in table.guests:
            for other in table.guests:
                if guest != other:
                    score += guest.get_preference(other)
        return score

    def _find_worst_table(self, plan):
        """Identify the table with the lowest average preference compatibility."""
        table_scores = []
        for i, table in enumerate(plan.tables):
            if len(table.guests) >= 2:
                score = self._calculate_table_score(plan, i)
                avg_score = score / (len(table.guests) * (len(table.guests) - 1))
                table_scores.append((i, avg_score))
        if table_scores:
            return min(table_scores, key=lambda x: x[1])[0]
        return random.randint(0, len(plan.tables) - 1)

    def _generate_neighbor(self, strategy=None):
        """Apply one of several perturbation strategies to generate a new seating arrangement."""
        if strategy is None:
            strategy = random.choice(['swap', 'move', 'reassign_cluster', 'table_shuffle', 'targeted_move'])

        new_plan = self.current_plan.copy()
        non_empty_tables = [i for i, t in enumerate(new_plan.tables) if t.guests]

        if not non_empty_tables:
            return new_plan, 'move'  # Nothing to change

        # Each block below applies a different strategy
        if strategy == 'swap' and len(non_empty_tables) >= 2:
            t1, t2 = random.sample(non_empty_tables, 2)
            if new_plan.tables[t1].guests and new_plan.tables[t2].guests:
                g1 = random.choice(new_plan.tables[t1].guests)
                g2 = random.choice(new_plan.tables[t2].guests)
                new_plan.tables[t1].remove_guest(g1)
                new_plan.tables[t2].remove_guest(g2)
                new_plan.tables[t1].add_guest(g2)
                new_plan.tables[t2].add_guest(g1)

        elif strategy == 'move':
            src = random.choice(non_empty_tables)
            guest = random.choice(new_plan.tables[src].guests)
            possible_targets = [i for i in range(len(new_plan.tables)) if i != src and not new_plan.tables[i].is_full()]
            if possible_targets:
                tgt = random.choice(possible_targets)
                new_plan.move_guest(guest, src, tgt)

        elif strategy == 'reassign_cluster':
            cluster_size = random.randint(2, 5)
            src = random.choice(non_empty_tables)
            guests = random.sample(new_plan.tables[src].guests, min(cluster_size, len(new_plan.tables[src].guests)))
            targets = [i for i in range(len(new_plan.tables)) if i != src and len(new_plan.tables[i].guests) + len(guests) <= new_plan.tables[i].capacity]
            if targets:
                tgt = random.choice(targets)
                for guest in guests:
                    new_plan.move_guest(guest, src, tgt)

        elif strategy == 'table_shuffle':
            if len(non_empty_tables) >= 2:
                tables = random.sample(non_empty_tables, min(3, len(non_empty_tables)))
                all_guests = []
                for t in tables:
                    all_guests.extend(new_plan.tables[t].guests.copy())
                    for g in new_plan.tables[t].guests.copy():
                        new_plan.tables[t].remove_guest(g)
                random.shuffle(all_guests)
                for guest in all_guests:
                    for t in tables:
                        if not new_plan.tables[t].is_full():
                            new_plan.tables[t].add_guest(guest)
                            break

        elif strategy == 'targeted_move':
            worst_idx = self._find_worst_table(new_plan)
            table = new_plan.tables[worst_idx]
            if len(table.guests) >= 2:
                worst_guest = min(table.guests, key=lambda g: sum(g.get_preference(o) for o in table.guests if o != g))
                best_target = None
                best_score = -float('inf')
                for i, t in enumerate(new_plan.tables):
                    if i != worst_idx and not t.is_full():
                        score = sum(worst_guest.get_preference(g) + g.get_preference(worst_guest) for g in t.guests)
                        if score > best_score:
                            best_score = score
                            best_target = i
                if best_target is not None:
                    new_plan.move_guest(worst_guest, worst_idx, best_target)

        return new_plan, strategy

    def _log_final_stats(self, elapsed_time):
        """Print and log summary statistics after optimization ends."""
        logging.info("=" * 50)
        logging.info("Simulated Annealing Complete")
        logging.info(f"Final best score: {self.best_score}")
        logging.info(f"Total runtime: {elapsed_time:.2f} seconds")
        logging.info(f"Iterations: {self.iterations}")

        logging.info("Strategy effectiveness:")
        for strategy, stats in self.perturbation_stats.items():
            a, i = stats['attempts'], stats['improvements']
            effectiveness = (i / a) * 100 if a else 0
            logging.info(f"  {strategy}: {i}/{a} successful ({effectiveness:.1f}%)")

        initial_score = self.history[0][1] if self.history else 0
        improvement = self.best_score - initial_score
        percent_improvement = (improvement / abs(initial_score)) * 100 if initial_score != 0 else float('inf')
        logging.info(f"Score improvement: {initial_score:.2f} → {self.best_score:.2f} (+{improvement:.2f}, {percent_improvement:.1f}%)")
        logging.info("=" * 50)