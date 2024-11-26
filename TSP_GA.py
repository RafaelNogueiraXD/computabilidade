import numpy as np
import random
from itertools import permutations
import matplotlib.pyplot as plt

class AlgoritmoGenetico:
    def __init__(self, nomes_cidades, 
                 coordenadas_cidades, 
                 tam_populacao=250, 
                 taxa_crossover=0.8, 
                 taxa_mutacao=0.2, 
                 num_geracoes=200):
        self.nomes_cidades : list[str] = nomes_cidades
        self.coordenadas_cidades = coordenadas_cidades
        self.tam_populacao = tam_populacao
        self.taxa_crossover = taxa_crossover
        self.taxa_mutacao = taxa_mutacao
        self.num_geracoes = num_geracoes

    def gerar_populacao_inicial(self):
        permutacoes_cidades = list(permutations(self.nomes_cidades))
        indices_aleatorios = random.sample(range(len(permutacoes_cidades)), self.tam_populacao)
        return [list(permutacoes_cidades[i]) for i in indices_aleatorios]

    def distancia_cidades(self, cidade1, cidade2):
        coord1 = self.coordenadas_cidades[cidade1]
        coord2 = self.coordenadas_cidades[cidade2]
        return np.linalg.norm(np.array(coord1) - np.array(coord2))

    def distancia_total(self, caminho):
        sum = 0
        for i in range(len(caminho) - 1):
            sum+=self.distancia_cidades(caminho[i], caminho[i+1])
        sum+=self.distancia_cidades(caminho[-1],caminho[0])
        return sum

    def calcular_fitness(self, populacao):
        distancias = np.array([self.distancia_total(caminho) for caminho in populacao])
        fitness = np.max(distancias) - distancias
        soma_fitness = np.sum(fitness)

        if soma_fitness == 0: 
            return np.ones(len(populacao)) / len(populacao) 

        return fitness / soma_fitness

    def selecao_roleta(self, populacao, prob_fitness):
        acumulado = prob_fitness.cumsum()
        indice = np.searchsorted(acumulado, random.random())
        return populacao[indice]

    def crossover(self, pai1, pai2):
        ponto_corte = random.randint(1, len(self.nomes_cidades) - 1)
        filho1 = pai1[:ponto_corte] + [cidade for cidade in pai2 if cidade not in pai1[:ponto_corte]]
        filho2 = pai2[:ponto_corte] + [cidade for cidade in pai1 if cidade not in pai2[:ponto_corte]]
        return filho1, filho2

    def mutacao(self, individuo):
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
        return individuo

    def executar(self):
        populacao = self.gerar_populacao_inicial()
        for geracao in range(self.num_geracoes):
            prob_fitness = self.calcular_fitness(populacao)
            pais = [self.selecao_roleta(populacao, prob_fitness) for _ in range(int(self.taxa_crossover * self.tam_populacao))]

            descendentes = []
            for i in range(0, len(pais), 2):
                if i+1 < len(pais):
                    filho1, filho2 = self.crossover(pais[i], pais[i+1])
                    if random.random() < self.taxa_mutacao:
                        filho1 = self.mutacao(filho1)
                    if random.random() < self.taxa_mutacao:
                        filho2 = self.mutacao(filho2)
                    descendentes.extend([filho1, filho2])

            populacao += descendentes
            populacao.sort(key=self.distancia_total)
            populacao = populacao[:self.tam_populacao]

        melhor_caminho = min(populacao, key=self.distancia_total)
        menor_distancia = self.distancia_total(melhor_caminho)
        return melhor_caminho, menor_distancia

def plotar_caminho_cidades(nomes_cidades, coordenadas, caminho):
    coordenadas_cidades = dict(zip(nomes_cidades, coordenadas))
    
    caminho.append(caminho[0])
    caminho_coords = [coordenadas_cidades[cidade] for cidade in caminho]

    plt.figure(figsize=(10, 6))
    x, y = zip(*caminho_coords) 
    plt.plot(x, y, marker='o', linestyle='-', color='blue', label="Caminho") 

    cidade_inicial = caminho[0]
    cx_inicial, cy_inicial = coordenadas_cidades[cidade_inicial]
    plt.scatter(cx_inicial, cy_inicial, color='red', s=100, label="Cidade Inicial") 

    for cidade, (cx, cy) in zip(caminho, caminho_coords):
        plt.text(cx, cy, cidade, fontsize=9, ha='right')

    plt.title("Caminho entre Cidades com Retorno")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(False)
    plt.legend()
    plt.show()

def main():
    # nomes_cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", 
    # "Salvador", "Curitiba", "Brasília", "Fortaleza", "Manaus", "Porto Alegre", "Recife"]
    # coordenadas = [(0, 0), (2, 1), (3, 4), (6, 7), (0, 6), (4, 3), (8, 6), (10, 8), (1, 8), (5, 9)]
    # coordenadas_cidades = dict(zip(nomes_cidades, coordenadas))
    nomes_cidades = ["Gliwice", "Cairo", "Rome", "Krakow", "Paris", "Alexandria", "Berlin", "Tokyo", "Rio", "Budapest"]
    coordenadas = [(0, 1), (3, 2), (6, 1), (7, 4.5), (15, -1), (10, 2.5), (16, 11), (5, 6), (8, 9), (1.5, 12)]
    coordenadas_cidades = dict(zip(nomes_cidades,coordenadas))

    algoritmo = AlgoritmoGenetico(nomes_cidades, coordenadas_cidades, tam_populacao=250
                                  , taxa_crossover=0.8, taxa_mutacao=0.2, num_geracoes=200)
    melhor_caminho, menor_distancia = algoritmo.executar()

    print("Melhor caminho:", melhor_caminho)
    print("Menor distância:", menor_distancia)
    plotar_caminho_cidades(nomes_cidades, coordenadas, melhor_caminho)

if __name__ == "__main__":
    main()
