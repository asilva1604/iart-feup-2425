import random
from seating_plan import SeatingPlan, Table

class KClustering:
    def __init__(self, guests, num_tables, table_capacity, max_iterations=100):
        self.guests = guests
        self.num_tables = num_tables
        self.table_capacity = table_capacity
        self.max_iterations = max_iterations

    def initialize_centroids(self):
        return random.sample(self.guests, self.num_tables)

    def assign_guests_to_tables(self, centroids):
        tables = [Table(self.table_capacity) for _ in range(self.num_tables)]
        guest_assigned = set()

        # Continue até todos os convidados serem atribuídos
        for guest in self.guests:
            # Preferência com centróides (bidirecional opcional)
            preferences = [
                guest.get_preference(centroid) + centroid.get_preference(guest)
                for centroid in centroids
            ]
            sorted_table_indices = sorted(range(self.num_tables), key=lambda idx: -preferences[idx])

            # Tenta colocar o convidado na mesa mais preferida com espaço
            for idx in sorted_table_indices:
                if not tables[idx].is_full():
                    tables[idx].add_guest(guest)
                    guest_assigned.add(guest)
                    break

        # Distribui convidados restantes (caso algum não tenha sido atribuído)
        unassigned = [g for g in self.guests if g not in guest_assigned]
        for guest in unassigned:
            for table in tables:
                if not table.is_full():
                    table.add_guest(guest)
                    break

        return tables

    def calculate_new_centroids(self, tables):
        centroids = []
        for table in tables:
            if not table.guests:
                centroids.append(random.choice(self.guests))
            else:
                centroids.append(
                    max(
                        table.guests,
                        key=lambda guest: sum(
                            guest.get_preference(other) + other.get_preference(guest)
                            for other in table.guests if guest != other
                        )
                    )
                )
        return centroids

    def run(self):
        centroids = self.initialize_centroids()
        best_plan = None
        best_score = float('-inf')

        for iteration in range(self.max_iterations):
            tables = self.assign_guests_to_tables(centroids)

            # Cria plano e atribui manualmente as mesas geradas
            seating_plan = SeatingPlan(self.guests, self.num_tables, self.table_capacity)
            seating_plan.tables = tables  # Substitui as mesas geradas aleatoriamente

            score = seating_plan.score()

            if score > best_score:
                best_score = score
                best_plan = seating_plan

            new_centroids = self.calculate_new_centroids(tables)

            if all(new_centroids[i].name == centroids[i].name for i in range(len(centroids))):
                break

            centroids = new_centroids

        return best_plan, best_score

