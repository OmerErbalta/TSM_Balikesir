import json
import random

class GeneticAlgorithm:
    def __init__(self, distances_matrix, pop_size=100, elite_percent=0.1, crossover_rate=0.7, mutation_rate=0.1):
        self.distances_matrix = distances_matrix
        self.pop_size = pop_size
        self.elite_percent = elite_percent
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def create_individual(self):
        return random.sample(range(20), 20)

    def fitness(self, individual):
        total_distance = sum(self.distances_matrix[individual[i]][individual[i+1]] for i in range(len(individual) - 1))
        return -total_distance
    def select_parents(self, population):
        tournament_size = 3
        participants = random.sample(population, tournament_size)
        return max(participants, key=lambda x: self.fitness(x))

    def ordered_crossover(self, parent1, parent2):
        size = len(parent1)
        start = random.randint(0, size - 1)
        end = random.randint(start + 1, size)
        child = [None] * size
        child[start:end] = parent1[start:end]
        remaining_genes = [gene for gene in parent2 if gene not in child[start:end]]
        remaining_index = 0

        for i in range(size):
            if child[i] is None:
                child[i] = remaining_genes[remaining_index]
                remaining_index += 1

        return child

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            index1, index2 = random.sample(range(len(individual)), 2)
            individual[index1], individual[index2] = individual[index2], individual[index1]
        return individual

    def elitism(self, population):
        elite_count = int(len(population) * self.elite_percent)
        elite = sorted(population, key=lambda x: self.fitness(x), reverse=True)[:elite_count]
        return elite

    def genetic_algorithm(self, generations):
        population = [self.create_individual() for _ in range(self.pop_size)]

        for generation in range(generations):
            population = sorted(population, key=lambda x: self.fitness(x), reverse=True)

            elite = self.elitism(population)

            new_population = elite.copy()

            for _ in range(self.pop_size - len(elite)):
                parent1 = self.select_parents(population)
                parent2 = self.select_parents(population)

                child = self.ordered_crossover(parent1, parent2)
                child = self.mutate(child)

                new_population.append(child)

            population = new_population

        best_individual = max(population, key=lambda x: self.fitness(x))
        return best_individual

def mesafeyiCek(i, j, mesafe_json):
    return mesafe_json[f'location {i}'][f'location_to {j}']

def genetic_algorithm_for_coordinates(json_file_path, pop_size=100, generations=1000, elite_percent=0.1, crossover_rate=0.7, mutation_rate=0.1):
    with open(json_file_path, 'r') as json_file:
        mesafe_json = json.load(json_file)

    distances_matrix = [[mesafeyiCek(i, j, mesafe_json) if i != j else 0 for j in range(20)] for i in range(20)]

    ga = GeneticAlgorithm(distances_matrix, pop_size=pop_size, elite_percent=elite_percent, crossover_rate=crossover_rate, mutation_rate=mutation_rate)
    best_route = ga.genetic_algorithm(generations)

    return best_route

