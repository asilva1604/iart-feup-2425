import math
import random
import logging
import time
from seating_plan import SeatingPlan

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimulatedAnnealing:
    def __init__(self, seating_plan, initial_temp=1000, cooling_rate=0.99, iterations=15000):
        self.current_plan = seating_plan
        self.best_plan = seating_plan.copy()
        self.current_score = seating_plan.score()
        self.best_score = self.current_score
        self.initial_temp = initial_temp
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.iterations = iterations
        self.no_improvement_count = 0
        self.max_no_improvement = 1000
        self.plateau_cooldown_factor = 0.8
        self.reheat_factor = 1.5
        self.history = []  # Store score history for analysis
        self.perturbation_stats = {
            'swap': {'attempts': 0, 'improvements': 0},
            'move': {'attempts': 0, 'improvements': 0},
            'reassign_cluster': {'attempts': 0, 'improvements': 0},
            'table_shuffle': {'attempts': 0, 'improvements': 0},
            'targeted_move': {'attempts': 0, 'improvements': 0}
        }

    def run(self):
        """Execute the simulated annealing optimization process."""
        start_time = time.time()
        logging.info(f"Starting optimization with initial score: {self.current_score}")
        logging.info(f"Parameters: T={self.initial_temp}, cooling_rate={self.cooling_rate}, iterations={self.iterations}")
        
        # Store initial state in history
        self.history.append((0, self.current_score, self.temp))
        
        for i in range(self.iterations):
            # Adaptive temperature adjustment
            if self.no_improvement_count > self.max_no_improvement:
                self._handle_optimization_plateau()
            
            # Select perturbation strategy based on current state
            strategy = self._select_perturbation_strategy(i)
            
            # Generate neighbor using selected strategy
            new_plan, strategy_used = self._generate_neighbor(strategy)
            new_score = new_plan.score()
            
            # Update strategy statistics
            self.perturbation_stats[strategy_used]['attempts'] += 1
            
            # Calculate the change in score
            delta = new_score - self.current_score
            
            # Determine whether to accept the new solution
            accept = False
            if delta > 0:
                accept = True
                self.perturbation_stats[strategy_used]['improvements'] += 1
                self.no_improvement_count = 0
            elif math.exp(delta / self.temp) > random.random():
                accept = True
                self.no_improvement_count += 1
            else:
                self.no_improvement_count += 1
            
            if accept:
                self.current_plan = new_plan
                self.current_score = new_score
                
                # Update best solution if needed
                if self.current_score > self.best_score:
                    self.best_plan = self.current_plan.copy()
                    self.best_score = self.current_score
                    logging.info(f"New best solution found: score = {self.best_score}")
            
            # Apply cooling schedule
            self.temp = self._cooling_schedule(i)
            
            # Log progress and store history
            if i % 200 == 0 or i == self.iterations - 1:
                elapsed = time.time() - start_time
                self.history.append((i, self.current_score, self.temp))
                logging.info(
                    f"Iteration {i}/{self.iterations} ({(i/self.iterations*100):.1f}%) - "
                    f"Temp: {self.temp:.4f}, Current: {self.current_score:.2f}, "
                    f"Best: {self.best_score:.2f}, Elapsed: {elapsed:.1f}s"
                )
        
        # Log final statistics
        self._log_final_stats(time.time() - start_time)
        
        return self.best_plan, self.best_score
    
    def _cooling_schedule(self, iteration):
        """Implement a non-linear cooling schedule."""
        # Linear progression from 0 to 1
        progress = iteration / self.iterations
        
        # Apply modified exponential cooling
        return self.initial_temp * (self.cooling_rate ** (1 + 2 * progress))
    
    def _handle_optimization_plateau(self):
        """Handle situations where optimization is stuck in a local optimum."""
        # Reset counter
        self.no_improvement_count = 0
        
        # Either cool down faster to accept a worse solution or reheat to explore more
        if random.random() < 0.7:  # 70% chance to cool faster
            self.temp *= self.plateau_cooldown_factor
            logging.info(f"Plateau detected: cooling faster, new temp = {self.temp:.4f}")
        else:  # 30% chance to reheat
            self.temp *= self.reheat_factor
            logging.info(f"Plateau detected: reheating, new temp = {self.temp:.4f}")
    
    def _select_perturbation_strategy(self, iteration):
        """
        Select perturbation strategy based on current optimization state.
        """
        # Early iterations: focus on exploration
        if iteration < self.iterations * 0.3:
            return random.choices(
                ['swap', 'move', 'reassign_cluster', 'table_shuffle', 'targeted_move'],
                weights=[0.3, 0.3, 0.2, 0.1, 0.1]
            )[0]
        # Middle iterations: balanced approach
        elif iteration < self.iterations * 0.7:
            return random.choices(
                ['swap', 'move', 'reassign_cluster', 'table_shuffle', 'targeted_move'],
                weights=[0.25, 0.25, 0.2, 0.15, 0.15]
            )[0]
        # Late iterations: focus more on local improvements
        else:
            return random.choices(
                ['swap', 'move', 'reassign_cluster', 'table_shuffle', 'targeted_move'],
                weights=[0.35, 0.3, 0.15, 0.1, 0.1]
            )[0]
    
    def _calculate_table_score(self, plan, table_idx):
        """Calculate the preference score for a specific table."""
        score = 0
        table = plan.tables[table_idx]
        for guest in table.guests:
            for other in table.guests:
                if guest != other:
                    score += guest.get_preference(other)
        return score
    
    def _find_worst_table(self, plan):
        """Find the table with the lowest average preference score."""
        table_scores = []
        for i, table in enumerate(plan.tables):
            # Only consider tables with at least 2 guests (to calculate preferences)
            if len(table.guests) >= 2:
                score = self._calculate_table_score(plan, i)
                avg_score = score / (len(table.guests) * (len(table.guests) - 1))  # Average per pair
                table_scores.append((i, avg_score))
        
        if table_scores:
            # Return the index of the table with the lowest average score
            return min(table_scores, key=lambda x: x[1])[0]
        
        # If no valid tables found, return a random table index
        return random.randint(0, len(plan.tables) - 1)
    
    def _generate_neighbor(self, strategy=None):
        """Generate a neighboring solution using various perturbation strategies."""
        if strategy is None:
            strategy = random.choice(['swap', 'move', 'reassign_cluster', 'table_shuffle', 'targeted_move'])
        
        new_plan = self.current_plan.copy()
        
        # Get non-empty tables
        non_empty_tables = [i for i, table in enumerate(new_plan.tables) if table.guests]
        
        if not non_empty_tables:
            return new_plan, 'move'  # No guests to move
        
        if strategy == 'swap' and len(non_empty_tables) >= 2:
            # Swap two guests between different tables
            table1, table2 = random.sample(non_empty_tables, 2)
            if new_plan.tables[table1].guests and new_plan.tables[table2].guests:
                guest1 = random.choice(new_plan.tables[table1].guests)
                guest2 = random.choice(new_plan.tables[table2].guests)
                new_plan.tables[table1].remove_guest(guest1)
                new_plan.tables[table2].remove_guest(guest2)
                new_plan.tables[table1].add_guest(guest2)
                new_plan.tables[table2].add_guest(guest1)
            
        elif strategy == 'move':
            # Move a single guest from one table to another
            source_table = random.choice(non_empty_tables)
            if new_plan.tables[source_table].guests:
                guest = random.choice(new_plan.tables[source_table].guests)
                possible_tables = [i for i in range(len(new_plan.tables)) if i != source_table and not new_plan.tables[i].is_full()]
                if possible_tables:
                    target_table = random.choice(possible_tables)
                    new_plan.move_guest(guest, source_table, target_table)
            
        elif strategy == 'reassign_cluster':
            # Move a cluster of related guests together
            cluster_size = random.randint(2, 5)
            source_table = random.choice(non_empty_tables)
            
            # Get guests from source table, limited by cluster size
            guests_to_move = []
            if new_plan.tables[source_table].guests:
                guests_to_move = random.sample(
                    new_plan.tables[source_table].guests, 
                    min(cluster_size, len(new_plan.tables[source_table].guests))
                )
            
            if guests_to_move:
                # Pick a target table that's different from the source and has capacity
                possible_tables = [i for i in range(len(new_plan.tables)) 
                                    if i != source_table and 
                                    len(new_plan.tables[i].guests) + len(guests_to_move) <= new_plan.tables[i].capacity]
                
                if possible_tables:
                    target_table = random.choice(possible_tables)
                    for guest in guests_to_move:
                        new_plan.move_guest(guest, source_table, target_table)
        
        elif strategy == 'table_shuffle':
            # Completely reorganize 2-3 tables
            if len(non_empty_tables) >= 2:
                # Select 2-3 tables to shuffle
                num_tables = min(random.randint(2, 3), len(non_empty_tables))
                tables_to_shuffle = random.sample(non_empty_tables, num_tables)
                
                # Collect all guests from these tables
                guests = []
                for table_idx in tables_to_shuffle:
                    guests.extend(new_plan.tables[table_idx].guests.copy())
                
                # Remove all guests from their tables
                for table_idx in tables_to_shuffle:
                    for guest in new_plan.tables[table_idx].guests.copy():
                        new_plan.tables[table_idx].remove_guest(guest)
                
                # Randomly reassign guests to the same set of tables
                random.shuffle(guests)
                for guest in guests:
                    # Find a table with space
                    available_tables = [idx for idx in tables_to_shuffle 
                                       if not new_plan.tables[idx].is_full()]
                    if available_tables:
                        target_table = random.choice(available_tables)
                        new_plan.tables[target_table].add_guest(guest)
                    else:
                        # If no space in shuffled tables, find another table
                        other_tables = [i for i in range(len(new_plan.tables)) 
                                       if i not in tables_to_shuffle and not new_plan.tables[i].is_full()]
                        if other_tables:
                            new_plan.tables[random.choice(other_tables)].add_guest(guest)
                        else:
                            # If all tables are full, add to the first shuffled table
                            # This shouldn't happen if the original plan was valid
                            new_plan.tables[tables_to_shuffle[0]].add_guest(guest)
        
        elif strategy == 'targeted_move':
            # Strategy to improve specific tables with low preference scores
            worst_table_idx = self._find_worst_table(new_plan)
            
            if worst_table_idx in non_empty_tables and len(new_plan.tables[worst_table_idx].guests) >= 2:
                # Find the guest with the lowest compatibility in this table
                lowest_compatibility_guest = None
                lowest_compatibility_score = float('inf')
                
                for guest in new_plan.tables[worst_table_idx].guests:
                    compatibility = 0
                    for other in new_plan.tables[worst_table_idx].guests:
                        if guest != other:
                            compatibility += guest.get_preference(other)
                    
                    # Average compatibility per other guest
                    avg_compatibility = compatibility / (len(new_plan.tables[worst_table_idx].guests) - 1)
                    
                    if avg_compatibility < lowest_compatibility_score:
                        lowest_compatibility_score = avg_compatibility
                        lowest_compatibility_guest = guest
                
                if lowest_compatibility_guest:
                    # Find a better table for this guest
                    best_target_table = None
                    best_compatibility_improvement = -float('inf')
                    
                    for table_idx in range(len(new_plan.tables)):
                        if table_idx != worst_table_idx and not new_plan.tables[table_idx].is_full():
                            # Calculate potential compatibility improvement
                            potential_improvement = 0
                            for potential_tablemate in new_plan.tables[table_idx].guests:
                                potential_improvement += (
                                    lowest_compatibility_guest.get_preference(potential_tablemate) +
                                    potential_tablemate.get_preference(lowest_compatibility_guest)
                                )
                            
                            if potential_improvement > best_compatibility_improvement:
                                best_compatibility_improvement = potential_improvement
                                best_target_table = table_idx
                    
                    if best_target_table is not None:
                        new_plan.move_guest(lowest_compatibility_guest, worst_table_idx, best_target_table)
        
        return new_plan, strategy
    
    def _log_final_stats(self, elapsed_time):
        """Log final statistics of the optimization run."""
        logging.info("=" * 50)
        logging.info("Simulated Annealing Complete")
        logging.info(f"Final best score: {self.best_score}")
        logging.info(f"Total runtime: {elapsed_time:.2f} seconds")
        logging.info(f"Iterations: {self.iterations}")
        
        # Calculate and log perturbation effectiveness
        logging.info("Strategy effectiveness:")
        for strategy, stats in self.perturbation_stats.items():
            attempts = stats['attempts']
            improvements = stats['improvements']
            if attempts > 0:
                effectiveness = (improvements / attempts) * 100
                logging.info(f"  {strategy}: {improvements}/{attempts} successful ({effectiveness:.1f}%)")
        
        # Score improvement
        initial_score = self.history[0][1] if self.history else 0
        improvement = self.best_score - initial_score
        percent_improvement = (improvement / abs(initial_score)) * 100 if initial_score != 0 else float('inf')
        logging.info(f"Score improvement: {initial_score:.2f} → {self.best_score:.2f} (+{improvement:.2f}, {percent_improvement:.1f}%)")
        logging.info("=" * 50)