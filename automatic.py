import os
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from src.genetic_algorithm import AlgoritmoGenetico
from src.visualization import plot_city_path

class GAPerformanceAnalyzer:
    def __init__(self, 
                 city_names, 
                 coordinates, 
                 num_runs=30, 
                 results_dir='results'):
        """
        Inicializa o analisador de desempenho do Algoritmo Genético.
        
        Args:
            city_names (list): Nomes das cidades
            coordinates (list): Coordenadas das cidades
            num_runs (int): Número de execuções
            results_dir (str): Diretório para salvar resultados
        """
        self.city_names = city_names
        self.coordinates = coordinates
        self.num_runs = num_runs
        self.results_dir = results_dir
        self.city_coordinates = dict(zip(city_names, coordinates))
        
        # Cria diretório de resultados se não existir
        os.makedirs(results_dir, exist_ok=True)

    def run_multiple_simulations(
        self, 
        population_sizes=[100, 250, 500],
        crossover_rates=[0.6, 0.8],
        mutation_rates=[0.1, 0.2],
        generations=[100, 200, 300]
    ):
        """
        Executa múltiplas simulações com diferentes configurações.
        
        Args:
            population_sizes (list): Tamanhos de população a testar
            crossover_rates (list): Taxas de crossover a testar
            mutation_rates (list): Taxas de mutação a testar
            generations (list): Números de gerações a testar
        
        Returns:
            list: Resultados detalhados das simulações
        """
        all_results = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(self.results_dir, f'ga_results_{timestamp}.csv')
        
        # Cabeçalho do arquivo CSV
        headers = [
            'Run', 'Population Size', 'Crossover Rate', 'Mutation Rate', 
            'Generations', 'Best Distance', 'Best Path'
        ]
        
        with open(results_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            
            # Contador para número total de simulações
            total_simulations = (
                len(population_sizes) * 
                len(crossover_rates) * 
                len(mutation_rates) * 
                len(generations) * 
                self.num_runs
            )
            current_simulation = 0
            
            # Testa todas as combinações
            for pop_size in population_sizes:
                for crossover_rate in crossover_rates:
                    for mutation_rate in mutation_rates:
                        for num_gen in generations:
                            # Executa múltiplas rodadas para cada configuração
                            for run in range(self.num_runs):
                                current_simulation += 1
                                print(f"Progresso: {current_simulation}/{total_simulations}")
                                
                                # Configura e roda o algoritmo genético
                                ga = AlgoritmoGenetico(
                                    self.city_names, 
                                    self.city_coordinates, 
                                    population_size=pop_size,
                                    crossover_rate=crossover_rate, 
                                    mutation_rate=mutation_rate, 
                                    generations=num_gen
                                )
                                
                                best_path, best_distance = ga.run()
                                
                                # Prepara resultado para salvar
                                result = [
                                    run + 1, 
                                    pop_size, 
                                    crossover_rate, 
                                    mutation_rate, 
                                    num_gen, 
                                    best_distance, 
                                    ' -> '.join(best_path)
                                ]
                                
                                # Salva no CSV
                                csvwriter.writerow(result)
                                csvfile.flush()
                                
                                all_results.append(result)
        
        # Gera visualizações
        self._generate_performance_plots(all_results, timestamp)
        
        return all_results

    def _generate_performance_plots(self, results, timestamp):
        """
        Gera gráficos de análise de desempenho.
        
        Args:
            results (list): Resultados das simulações
            timestamp (str): Timestamp para identificação dos gráficos
        """
        results_df = np.array(results)
        
        # Gráfico de dispersão: Tamanho da população vs Distância
        plt.figure(figsize=(10, 6))
        pop_sizes = results_df[:, 1].astype(float)
        distances = results_df[:, 5].astype(float)
        plt.scatter(pop_sizes, distances, alpha=0.5)
        plt.title('População vs Distância')
        plt.xlabel('Tamanho da População')
        plt.ylabel('Distância')
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, f'population_distance_{timestamp}.png'))
        plt.close()
        
        # Gráfico de caixa: Taxas de crossover vs Distância
        plt.figure(figsize=(10, 6))
        crossover_rates = results_df[:, 2].astype(float)
        distances = results_df[:, 5].astype(float)
        unique_rates = np.unique(crossover_rates)
        box_data = [distances[crossover_rates == rate] for rate in unique_rates]
        plt.boxplot(box_data, labels=[str(rate) for rate in unique_rates])
        plt.title('Taxas de Crossover vs Distância')
        plt.xlabel('Taxa de Crossover')
        plt.ylabel('Distância')
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, f'crossover_distance_{timestamp}.png'))
        plt.close()

def main():
    # Dados das cidades
    city_names = ["Gliwice", "Cairo", "Rome", "Krakow", "Paris", 
                  "Alexandria", "Berlin", "Tokyo", "Rio", "Budapest"]
    coordinates = [
        (0, 1), (3, 2), (6, 1), (7, 4.5), (15, -1), 
        (10, 2.5), (16, 11), (5, 6), (8, 9), (1.5, 12)
    ]

    # Inicializa o analisador
    analyzer = GAPerformanceAnalyzer(
        city_names, 
        coordinates, 
        num_runs=30,  # Número de execuções para cada configuração
        results_dir='performance_results'
    )

    # Executa múltiplas simulações
    results = analyzer.run_multiple_simulations(
        population_sizes=[100, 250, 500],
        crossover_rates=[0.6, 0.8],
        mutation_rates=[0.1, 0.2],
        generations=[100, 200, 300]
    )

    # Sumário dos resultados
    print("\nResumo dos Resultados:")
    min_distance = min(float(result[5]) for result in results)
    max_distance = max(float(result[5]) for result in results)
    avg_distance = sum(float(result[5]) for result in results) / len(results)
    
    print(f"Menor distância encontrada: {min_distance:.2f}")
    print(f"Maior distância encontrada: {max_distance:.2f}")
    print(f"Média de distância: {avg_distance:.2f}")

if __name__ == "__main__":
    main()