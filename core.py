import random
from scipy.spatial import distance

INF = float('inf')

class GenAlgorithm:
    def __init__(self, points, cluster_count=5, population_size=50, steps=10):
        self.points = points
        self.cluster_count = cluster_count
        self.population_size = population_size
        self.steps = steps
        self.chromosomes = list()

    def initial_population(self):
        for i in range(self.population_size):
            chromosome = list()
            for j in range(len(self.points)):
                chromosome.append(random.randint(1, self.cluster_count))
            chromosome.append(self.cluster_count)
            self.chromosomes.append(chromosome)

    def mutate(self, chromosome):
        idx = random.randint(0, len(self.points)-1)
        cur_dist = INF
        selected_label = chromosome[idx]
        for i in range(len(self.points)):
            if i==idx:
                continue
            dist = distance.euclidean(self.points[idx], self.points[i])
            if dist < cur_dist:
                cur_dist = dist
                selected_label = chromosome[i]
        chromosome[idx] = selected_label

        idx = random.randint(0, len(self.points)-1)
        label = random.randint(1, self.cluster_count)
        chromosome[idx] = label
        return chromosome

    def crossover(self, parent1, parent2):
        idx = random.randint(1, len(self.points)-1)
        child1 = parent1[:idx] + parent2[idx:]
        child2 = parent2[:idx] + parent1[idx:]
        return child1, child2

    def get_fitness(self, chromosome):
        cluster_points = dict()
        for idx, val in enumerate(chromosome[:len(self.points)]):
            if val not in cluster_points:
                cluster_points[val] = list()
            cluster_points[val].append(idx)
        result = 0
        for key, val in cluster_points.items():
            for i in range(len(val)):
                for j in range(i):
                    result += distance.euclidean(self.points[i], self.points[j])
        return result

    def run(self):
        self.initial_population()
        filter_count = int(self.population_size / 5)  # 20% of the best
        chromosomes = self.chromosomes
        for _ in range(self.steps):
            chromosomes = sorted(chromosomes, key=lambda chromosome: self.get_fitness(chromosome))
            chromosomes = chromosomes[:filter_count]
            print(f"#step {_}")
            for i in range(5):
                print(self.get_fitness(chromosomes[i]))
            print()

            # cross over
            while len(chromosomes) < self.population_size:
                parent1 = random.choice(chromosomes)
                parent2 = random.choice(chromosomes)
                child1, child2 = self.crossover(parent1, parent2)
                chromosomes.append(child1)
                if len(chromosomes) < self.population_size:
                    chromosomes.append(child2)

            # mutation
            for _ in range(int(self.population_size/2)):
                idx = random.randint(0, self.population_size-1)
                chromosomes[idx] = self.mutate(chromosomes[idx])
        chromosomes = sorted(chromosomes, key=lambda chromosome: self.get_fitness(chromosome))
        print(filter_count)
        return chromosomes[:filter_count]
