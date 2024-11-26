from src.genetic_algorithm import TravelingSalesmanGeneticAlgorithm
from src.visualization import plot_city_path

def main():
    # Dados das cidades
    city_names = ["Gliwice", "Cairo", "Rome", "Krakow", "Paris", 
                  "Alexandria", "Berlin", "Tokyo", "Rio", "Budapest"]
    coordinates = [
        (0, 1), (3, 2), (6, 1), (7, 4.5), (15, -1), 
        (10, 2.5), (16, 11), (5, 6), (8, 9), (1.5, 12)
    ]
    city_coordinates = dict(zip(city_names, coordinates))

    # Configuração do Algoritmo Genético
    ga = TravelingSalesmanGeneticAlgorithm(
        city_names, 
        city_coordinates, 
        population_size=250,
        crossover_rate=0.8, 
        mutation_rate=0.2, 
        generations=200
    )

    # Executa o algoritmo
    best_path, best_distance = ga.run()

    # Imprime resultados
    print("Best path:", best_path)
    print("Shortest distance:", best_distance)

    # Visualiza o caminho
    plot_city_path(city_names, coordinates, best_path)

if __name__ == "__main__":
    main()