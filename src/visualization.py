import matplotlib.pyplot as plt

def plot_city_path(city_names, coordinates, path):
    """
    Plota o caminho das cidades.
    
    Args:
        city_names (list): Nomes das cidades
        coordinates (list): Coordenadas das cidades
        path (list): Caminho percorrido
    """
    city_coordinates = dict(zip(city_names, coordinates))
    
    # Adiciona o primeiro ponto no final para fechar o ciclo
    complete_path = path + [path[0]]
    path_coords = [city_coordinates[city] for city in complete_path]

    plt.figure(figsize=(10, 6))
    x, y = zip(*path_coords)
    plt.plot(x, y, marker='o', linestyle='-', color='blue', label="Path")

    # Destaca a cidade inicial
    start_city = complete_path[0]
    cx_start, cy_start = city_coordinates[start_city]
    plt.scatter(cx_start, cy_start, color='red', s=100, label="Start City")

    # Adiciona labels das cidades
    for city, (cx, cy) in zip(complete_path, path_coords):
        plt.text(cx, cy, city, fontsize=9, ha='right')

    plt.title("Cities Path with Return")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(False)
    plt.legend()
    plt.show()