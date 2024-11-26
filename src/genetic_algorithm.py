import random
import numpy as np
from itertools import permutations
from .distance_calculator import distancia_total

class AlgoritmoGenetico:
    """
    Implementação de Algoritmo Genético para o Problema do Caixeiro Viajante.
    """
    def __init__(self, city_names, city_coordinates, 
                 population_size=250, 
                 crossover_rate=0.8, 
                 mutation_rate=0.2, 
                 generations=200,
                 tournament_size=3):
        """
        Inicializa o Algoritmo Genético.
        
        Args:
            city_names (list): Nomes das cidades
            city_coordinates (dict): Coordenadas das cidades
            population_size (int): Tamanho da população
            crossover_rate (float): Taxa de crossover
            mutation_rate (float): Taxa de mutação
            generations (int): Número de gerações
            tournament_size (int): Número de indivíduos no torneio
        """
        self.city_names = city_names
        self.city_coordinates = city_coordinates
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.tournament_size = tournament_size
    def gerar_populacao_inicial(self):
        """
        Gera população inicial de caminhos possíveis.
        
        Returns:
            list: População inicial de caminhos
        """
        city_permutations = list(permutations(self.city_names))
        random_indices = random.sample(range(len(city_permutations)), self.population_size)
        return [list(city_permutations[i]) for i in random_indices]

    def calcular_fitness(self, population):
        """
        Calcula o fitness da população.
        
        Args:
            population (list): População de caminhos
        
        Returns:
            numpy.ndarray: Probabilidades de fitness
        """
        distances = np.array([
            distancia_total(path, self.city_coordinates) 
            for path in population
        ])
        
        fitness = np.max(distances) - distances
        fitness_sum = np.sum(fitness)

        return fitness / fitness_sum if fitness_sum != 0 else np.ones(len(population)) / len(population)
    def selecao_torneio(self, population):
        """
        Método de seleção por torneio.
        
        Args:
            population (list): População de caminhos
        
        Returns:
            list: Caminho selecionado como o melhor do torneio
        """
        # Seleciona aleatoriamente tournament_size indivíduos
        tournament_candidates = random.sample(population, self.tournament_size)
        
        # Encontra o melhor (caminho com menor distância)
        best_candidate = min(
            tournament_candidates, 
            key=lambda path: distancia_total(path, self.city_coordinates)
        )
        
        return best_candidate
    def selecao_roleta(self, population, fitness_probabilities):
        """
        Seleção por roleta.
        
        Args:
            population (list): População de caminhos
            fitness_probabilities (numpy.ndarray): Probabilidades de fitness
        
        Returns:
            list: Caminho selecionado
        """
        cumulative = fitness_probabilities.cumsum()
        index = np.searchsorted(cumulative, random.random())
        return population[index]

    def crossover(self, parent1, parent2):
        """
        Realiza crossover entre dois pais.
        
        Args:
            parent1 (list): Primeiro pai
            parent2 (list): Segundo pai
        
        Returns:
            tuple: Dois filhos gerados
        """
        cut_point = random.randint(1, len(self.city_names) - 1)
        
        child1 = parent1[:cut_point] + [city for city in parent2 if city not in parent1[:cut_point]]
        child2 = parent2[:cut_point] + [city for city in parent1 if city not in parent2[:cut_point]]
        
        return child1, child2

    def mutacao(self, individual):
        """
        Aplica mutação em um indivíduo.
        
        Args:
            individual (list): Caminho a ser mutado
        
        Returns:
            list: Caminho mutado
        """
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
        return individual

    def run(self):
        """
        Executa o algoritmo genético.
        
        Returns:
            tuple: Melhor caminho e menor distância
        """
        population = self.gerar_populacao_inicial()
        
        for _ in range(self.generations):
            fitness_probabilities = self.calcular_fitness(population)
            
            parents = [
                self.selecao_roleta(population, fitness_probabilities)
                for _ in range(int(self.crossover_rate * self.population_size))
            ]

            offspring = []
            for i in range(0, len(parents), 2):
                if i + 1 < len(parents):
                    child1, child2 = self.crossover(parents[i], parents[i+1])
                    
                    child1 = self.mutacao(child1) if random.random() < self.mutation_rate else child1
                    child2 = self.mutacao(child2) if random.random() < self.mutation_rate else child2
                    
                    offspring.extend([child1, child2])

            population += offspring
            population.sort(key=lambda path: distancia_total(path, self.city_coordinates))
            population = population[:self.population_size]

        best_path = min(population, key=lambda path: distancia_total(path, self.city_coordinates))
        best_distance = distancia_total(best_path, self.city_coordinates)
        
        return best_path, best_distance