import numpy as np

def distancia_cidades(coord1, coord2):
    """
    Calcula a distância euclidiana entre duas coordenadas.
    
    Args:
        coord1 (tuple): Coordenadas do primeiro ponto
        coord2 (tuple): Coordenadas do segundo ponto
    
    Returns:
        float: Distância entre os pontos
    """
    return np.linalg.norm(np.array(coord1) - np.array(coord2))

def distancia_total(path, coordinates):
    """
    Calcula a distância total de um caminho, incluindo o retorno ao ponto inicial.
    
    Args:
        path (list): Lista de cidades no caminho
        coordinates (dict): Dicionário de coordenadas das cidades
    
    Returns:
        float: Distância total do caminho
    """
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distancia_cidades(coordinates[path[i]], coordinates[path[i+1]])
    
    # Adiciona a distância de volta à cidade inicial para completar o ciclo
    total_distance += distancia_cidades(
        coordinates[path[-1]], 
        coordinates[path[0]]
    )
    
    return total_distance